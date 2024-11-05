import os
import json
import asyncio
import threading
import time
from dataclasses import dataclass, field, asdict
from typing import Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketState

if os.environ.get("NO_DEVICE"):
    from api.conftest import MockedPSU as PSU
else:
    from hantekpsu import PSU

psu_limits = {"HDP1160V4S": {"MAX_VOLTAGE": 160, "MAX_CURRENT": 4.1}}

psu = PSU()


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=psu_data_fetcher).start()
    yield


app = FastAPI(lifespan=lifespan)

ws_clients = []


@dataclass
class LiveValue:
    value: Any = None
    is_stale: bool = True


@dataclass
class LiveData:
    is_on: LiveValue = field(default_factory=LiveValue)
    active_voltage: LiveValue = field(default_factory=LiveValue)
    active_current: LiveValue = field(default_factory=LiveValue)
    voltage_limit: LiveValue = field(default_factory=LiveValue)
    current_limit: LiveValue = field(default_factory=LiveValue)
    max_voltage: LiveValue = field(default_factory=LiveValue)
    max_current: LiveValue = field(default_factory=LiveValue)

    def update(self, name: str, value: Any):
        setattr(self, name, LiveValue(value=value, is_stale=False))

    def mark_stale(self, name: str):
        getattr(self, name).is_stale = True

    def values(self):
        return [v["value"] for v in asdict(self).values()]


live_data = LiveData()


class InvalidPSUException(Exception):
    pass


def get_psu_limits():
    model = psu.get_model()
    if model not in psu_limits:
        raise InvalidPSUException(f"Model '{model}' is not supported")
    max_voltage = psu_limits[model]["MAX_VOLTAGE"]
    max_current = psu_limits[model]["MAX_CURRENT"]
    return (max_voltage, max_current)


def psu_data_fetcher():
    while True:
        try:
            if live_data.max_voltage.value is None:
                max_voltage, max_current = get_psu_limits()
                live_data.update("max_voltage", max_voltage)
                live_data.update("max_current", max_current)
            time.sleep(1)
            live_data.mark_stale("is_on")
            live_data.mark_stale("active_voltage")
            live_data.mark_stale("active_current")
            live_data.mark_stale("voltage_limit")
            live_data.mark_stale("current_limit")
            is_on = psu.get_on_off_status()
            if live_data.is_on.is_stale:
                live_data.update("is_on", is_on)
            active_voltage = psu.get_active_voltage()
            if live_data.active_voltage.is_stale:
                live_data.update("active_voltage", active_voltage)
            active_current = psu.get_active_current()
            if live_data.active_current.is_stale:
                live_data.update("active_current", active_current)
            voltage_limit = psu.get_voltage_limit()
            if live_data.voltage_limit.is_stale:
                live_data.update("voltage_limit", voltage_limit)
            current_limit = psu.get_current_limit()
            if live_data.current_limit.is_stale:
                live_data.update("current_limit", current_limit)
        except Exception as e:
            print(e)
            import traceback

            traceback.print_exc()


async def send_psu_status(websocket: WebSocket):
    while websocket.application_state == WebSocketState.CONNECTED and websocket in ws_clients:
        (
            is_on,
            active_voltage,
            active_current,
            voltage_limit,
            current_limit,
            max_voltage,
            max_current,
        ) = live_data.values()
        if is_on is not None:
            await websocket.send_text(json.dumps({"status": "OK", "command": "POWER", "payload": is_on}))
        if active_voltage is not None:
            await websocket.send_text(json.dumps({"status": "OK", "command": "VOLTAGE", "payload": active_voltage}))
        if active_current is not None:
            await websocket.send_text(json.dumps({"status": "OK", "command": "CURRENT", "payload": active_current}))
        if voltage_limit is not None:
            await websocket.send_text(
                json.dumps(
                    {
                        "status": "OK",
                        "command": "VOLTAGE_LIMIT",
                        "payload": voltage_limit,
                    }
                )
            )
        if current_limit is not None:
            await websocket.send_text(
                json.dumps(
                    {
                        "status": "OK",
                        "command": "CURRENT_LIMIT",
                        "payload": current_limit,
                    }
                )
            )
        if max_voltage is not None:
            await websocket.send_text(json.dumps({"status": "OK", "command": "MAX_VOLTAGE", "payload": max_voltage}))
        if max_current is not None:
            await websocket.send_text(json.dumps({"status": "OK", "command": "MAX_CURRENT", "payload": max_current}))
        await asyncio.sleep(1)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        ws_clients.append(websocket)
        await websocket.accept()
        asyncio.create_task(send_psu_status(websocket))
        while websocket.application_state == WebSocketState.CONNECTED:
            message = await websocket.receive_text()
            data = json.loads(message)
            command = data["command"]
            if command == "POWER_ON":
                psu.turn_on()
                live_data.update("is_on", True)
                await websocket.send_text(
                    json.dumps(
                        {
                            "status": "OK",
                            "command": "POWER",
                            "payload": live_data.is_on.value,
                        }
                    )
                )
            if command == "POWER_OFF":
                psu.turn_off()
                live_data.update("is_on", False)
                await websocket.send_text(
                    json.dumps(
                        {
                            "status": "OK",
                            "command": "POWER",
                            "payload": live_data.is_on.value,
                        }
                    )
                )
            if command == "SET_VOLTAGE":
                psu.set_output_voltage(data["payload"])
                live_data.update("voltage_limit", data["payload"])
            if command == "SET_CURRENT":
                psu.set_output_current(data["payload"])
                live_data.update("current_limit", data["payload"])
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except InvalidPSUException:
        await websocket.send_text(json.dumps({"status": "ERROR", "message": "Model not supported"}))
        await websocket.close()
    finally:
        ws_clients.remove(websocket)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
