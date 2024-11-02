import os
import json
import asyncio
from time import sleep
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketState

if os.environ.get("NO_DEVICE"):
    from api.conftest import MockedPSU as PSU
else:
    from hantekpsu import PSU

psu_limits = {
    "HDP1160V4S": {
        "MAX_VOLTAGE": 160,
        "MAX_CURRENT": 4.1
    }
}

app = FastAPI()
psu = PSU()

ws_clients = []

class InvalidPSUException(Exception):
    pass

def get_psu_limits():
    model = psu.get_model()
    if model not in psu_limits:
        raise InvalidPSUException
    max_voltage = psu_limits[model]["MAX_VOLTAGE"]
    max_current = psu_limits[model]["MAX_CURRENT"]
    return (max_voltage, max_current)

def get_psu_live_data():
    return (
        psu.get_on_off_status(),
        psu.get_active_voltage(),
        psu.get_active_current(),
        psu.get_voltage_limit(),
        psu.get_current_limit(),
    )

async def send_psu_status(websocket: WebSocket):
    while websocket.application_state == WebSocketState.CONNECTED and websocket in ws_clients:
        is_on, active_voltage, active_current, voltage_limit, current_limit = get_psu_live_data()
        await websocket.send_text(json.dumps({"status": "OK", "command": "POWER", "payload": is_on}))
        await websocket.send_text(json.dumps({"status": "OK", "command": "VOLTAGE", "payload": active_voltage}))
        await websocket.send_text(json.dumps({"status": "OK", "command": "CURRENT", "payload": active_current}))
        await websocket.send_text(json.dumps({"status": "OK", "command": "VOLTAGE_LIMIT", "payload": voltage_limit}))
        await websocket.send_text(json.dumps({"status": "OK", "command": "CURRENT_LIMIT", "payload": current_limit}))
        await asyncio.sleep(1)

async def send_initial_data(websocket: WebSocket, max_voltage, max_current, is_on):
    await websocket.send_text(json.dumps({"status": "OK", "command": "MAX_VOLTAGE", "payload": max_voltage}))
    await websocket.send_text(json.dumps({"status": "OK", "command": "MAX_CURRENT", "payload": max_current}))
    await websocket.send_text(json.dumps({"status": "OK", "command": "POWER", "payload": is_on}))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        ws_clients.append(websocket)
        await websocket.accept()
        max_voltage, max_current = get_psu_limits()
        await send_initial_data(websocket, max_voltage, max_current, psu.get_on_off_status())
        asyncio.create_task(send_psu_status(websocket))
        while websocket.application_state == WebSocketState.CONNECTED:
            message = await websocket.receive_text()
            data = json.loads(message)
            command = data['command']
            if command == "POWER_ON":
                psu.turn_on()
                await websocket.send_text(json.dumps({"status": "OK", "command": "POWER", "payload": psu.get_on_off_status()}))
            if command == "POWER_OFF":
                psu.turn_off()
                await websocket.send_text(json.dumps({"status": "OK", "command": "POWER", "payload": psu.get_on_off_status()}))
            if command == "SET_VOLTAGE":
                psu.set_output_voltage(data['payload'])
            if command == "SET_CURRENT":
                psu.set_output_current(data['payload'])
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except InvalidPSUException:
        await websocket.send_text(json.dumps({"status": "ERROR", "message": "Model not supported"}))
        await websocket.close()
    finally:
        ws_clients.remove(websocket)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
