import os
import pytest
from fastapi.testclient import TestClient
import json
from unittest.mock import patch
from unittest.mock import MagicMock

os.environ["NO_DEVICE"] = "1"

if not os.path.exists("static"):
    os.makedirs("static")

from api.ws import app

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def ensure_static_files_exist():
    if not os.path.exists("static/index.html"):
        with open("static/index.html", "w") as f:
            f.write("<html></html>")
    yield
    os.remove("static/index.html")
    os.rmdir("static")


def test_serves_html_on_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html>" in response.text


@pytest.mark.asyncio
async def test_processes_power_on_command():
    mock_psu = MagicMock()
    with patch("api.ws.psu", mock_psu):
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text(json.dumps({"command": "POWER_ON"}))
            response = websocket.receive_text()
            response_data = json.loads(response)
            assert response_data == {"status": "OK", "command": "POWER", "payload": True}
            mock_psu.turn_on.assert_called_once()
