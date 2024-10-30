import os
import pytest

from api.ws import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def ensure_static_files_exist():
    if not os.path.exists("static"):
        os.makedirs("static")
    if not os.path.exists("static/index.html"):
        with open("static/index.html", "w") as f:
            f.write("<html></html>")

def test_serves_html_on_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html>" in response.text