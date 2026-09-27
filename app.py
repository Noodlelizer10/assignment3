import json
import time
import uuid
from copy import deepcopy
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("posts.json")
BASE_TIME = int(time.time() * 1000)
DEFAULT_POSTS = [
    {
        "id": "starter-1",
        "author": "Maya Chen",
        "initials": "MC",
        "text": "A reminder that small progress is still progress. Taking the long way today.",
        "createdAt": BASE_TIME - 18 * 60 * 1000,
        "likes": 12,
        "liked": False,
        "comments": [
            {
                "id": "comment-1",
                "author": "Jordan Davis",
                "text": "Love this.",
                "createdAt": BASE_TIME - 12 * 60 * 1000,
            }
        ],
    },
    {
        "id": "starter-2",
        "author": "Alex Rivera",
        "initials": "AR",
        "text": "Just made the best grilled cheese of my life. The secret was patience.",
        "createdAt": BASE_TIME - 47 * 60 * 1000,
        "likes": 8,
        "liked": False,
        "comments": [],
    },
]


def save_posts(posts):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False)


def load_posts():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                posts = json.load(file)
            if isinstance(posts, list):
                return posts
        except (json.JSONDecodeError, OSError):
            pass

    save_posts(deepcopy(DEFAULT_POSTS))
    return deepcopy(DEFAULT_POSTS)


def format_time(timestamp):
    seconds = max(0, int((time.time() * 1000 - int(timestamp)) / 1000))
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def sort_posts(posts, newest_first):
    return sorted(posts, key=lambda item: item["createdAt"], reverse=newest_first)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        if request.form.get("action") == "create" and text:
            posts = load_posts()
            posts.insert(
                0,
                {
                    "id": str(uuid.uuid4()),
                    "author": "Jordan Davis",
                    "initials": "JD",
                    "text": text,
                    "createdAt": int(time.time() * 1000),
                    "likes": 0,
                    "liked": False,
                },
            )
            save_posts(posts)
            return redirect(url_for("index", sort="newest"))

    sort_value = request.args.get("sort", "newest")
    newest_first = sort_value != "oldest"
    posts = sort_posts(load_posts(), newest_first)
    return render_template(
        "index.html",
        posts=posts,
        newest_first=newest_first,
        format_time=format_time,
    )


@app.route("/like/<post_id>", methods=["POST"])
def toggle_like(post_id):
    sort_value = request.form.get("sort", "newest")
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["liked"] = not post["liked"]
            post["likes"] += 1 if post["liked"] else -1
            break
    save_posts(posts)
    return redirect(url_for("index", sort=sort_value))


@app.route("/comment/<post_id>", methods=["POST"])
def add_comment(post_id):
    sort_value = request.form.get("sort", "newest")
    text = (request.form.get("text") or "").strip()
    if text:
        posts = load_posts()
        for post in posts:
            if post["id"] == post_id:
                post.setdefault("comments", []).append(
                    {
                        "id": str(uuid.uuid4()),
                        "author": "Jordan Davis",
                        "text": text,
                        "createdAt": int(time.time() * 1000),
                    }
                )
                break
        save_posts(posts)
    return redirect(url_for("index", sort=sort_value))


if __name__ == "__main__":
    app.run(debug=True)
