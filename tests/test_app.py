import pytest

from app import app, DATA_FILE, load_posts


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "posts.json"
    monkeypatch.setattr("app.DATA_FILE", data_file)
    monkeypatch.setattr("app.DEFAULT_POSTS", [
        {
            "id": "starter-1",
            "author": "Maya Chen",
            "initials": "MC",
            "text": "A reminder that small progress is still progress.",
            "createdAt": 1700000000000,
            "likes": 12,
            "liked": False,
            "comments": [
                {"id": "comment-1", "author": "Jordan Davis", "text": "Love this.", "createdAt": 1700000001000}
            ],
        }
    ])
    with app.test_client() as client:
        yield client


def test_homepage_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Community feed" in response.data


def test_create_post(client):
    response = client.post("/", data={"action": "create", "text": "Hello from Python"})
    assert response.status_code == 302
    posts = load_posts()
    assert any(post["text"] == "Hello from Python" for post in posts)


def test_like_post(client):
    post = load_posts()[0]
    response = client.post(f"/like/{post['id']}")
    assert response.status_code == 302
    updated = load_posts()[0]
    assert updated["likes"] == post["likes"] + 1


def test_comment_post(client):
    post = load_posts()[0]
    response = client.post(f"/comment/{post['id']}", data={"text": "This is a thoughtful post."})
    assert response.status_code == 302
    updated = load_posts()[0]
    assert any(comment["text"] == "This is a thoughtful post." for comment in updated["comments"])
