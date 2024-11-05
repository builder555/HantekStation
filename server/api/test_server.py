import os
import pytest
from fastapi.testclient import TestClient

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
