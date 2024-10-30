import os
import json
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    model = psu.get_model()
    if model not in psu_limits:
        await websocket.send_text(json.dumps({"status": "ERROR", "message": "Model not supported"}))
        await websocket.close()
        return
    is_on = psu.get_on_off_status()
    max_voltage = psu_limits[model]["MAX_VOLTAGE"]
    max_current = psu_limits[model]["MAX_CURRENT"]
    await websocket.send_text(json.dumps({"status": "OK", "command": "MAX_VOLTAGE", "payload": max_voltage}))
    await websocket.send_text(json.dumps({"status": "OK", "command": "MAX_CURRENT", "payload": max_current}))
    await websocket.send_text(json.dumps({"status": "OK", "command": "POWER", "payload": is_on}))
    try:
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

app.mount("/", StaticFiles(directory="static", html=True), name="static")
