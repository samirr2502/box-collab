from server.server import app  # Import your Flask app
import pytest
from unittest.mock import patch

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_serves_index_html(client):
    """Should return index.html when path is empty"""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<html" in rv.data  # Rough check that HTML is served

def test_index_serves_static_file(client, tmp_path, monkeypatch):
    """Should return an existing file if found in TEMPLATE_DIR"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")

    monkeypatch.setattr("server.TEMPLATE_DIR", str(tmp_path))
    rv = client.get("/test.txt")
    assert rv.status_code == 200
    assert rv.data == b"hello world"

@patch("api_get_auth_code.main")
def test_get_box_access(mock_api, client):
    """Should call api_get_auth_code.main()"""
    mock_api.return_value = "some_response"
    rv = client.get("/get_box_access")
    assert rv.status_code == 200 or rv.status_code == 302

@patch("api_connect.get_access_token")
def test_get_auth_token_redirect(mock_get_token, client, monkeypatch):
    """Should exchange auth code and redirect with tokens"""
    mock_get_token.return_value = ("access123", "refresh456")
    monkeypatch.setitem(app.config, "SERVER_NAME", "localhost")

    rv = client.get("/auth?code=fakecode")
    assert rv.status_code == 302
    assert "refreshToken=refresh456" in rv.location
    assert "accessToken=access123" in rv.location

@patch("api_connect.get_access_token")
@patch("terminal_view.run")
def test_get_auth_token_term(mock_terminal, mock_get_token, client):
    """Should call terminal_view.run() after getting tokens"""
    mock_get_token.return_value = ("access123", "refresh456")
    rv = client.get("/auth_terminal?code=fakecode")
    assert rv.status_code == 200
    mock_terminal.assert_called_once()

@patch("get_collabs.main")
def test_get_collabs(mock_collabs, client):
    """Should call get_collabs.main with given params"""
    rv = client.get("/get_collabs?folderId=123&excludeFolderIds=456&refreshToken=rtoken&accessToken=atoken")
    assert rv.status_code == 200
    assert rv.json["status"] == "success"
    mock_collabs.assert_called_with("atoken", "rtoken", "123", "456")

@patch("get_items.main")
def test_get_items(mock_items, client):
    """Should return items from get_items.main"""
    mock_items.return_value = [{"id": "1", "name": "testfile"}]
    rv = client.get("/get_items?folderId=123&refreshToken=rtoken&accessToken=atoken")
    assert rv.status_code == 200
    assert rv.json == [{"id": "1", "name": "testfile"}]
    mock_items.assert_called_with("atoken", "rtoken", "123")
