import shelve
from enum import Enum

from flask import Flask, g, redirect, url_for, render_template

DB_FILE = "tasklet"


class Priorities(Enum):
    Green = 0
    Blue = 1
    Yellow = 2
    Red = 3


class Tasklet:
    text = ""
    priority = Priorities.Green
    done = False

    def __init__(self, text, priority=Priorities.Green, done=False):
        self.text = text
        self.priority = priority
        self.done = done

app = Flask(__name__)


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = shelve.open(DB_FILE, writeback=True)
        if "tasklets" not in db:
            db["tasklets"] = []
    return db


@app.route("/")
def list_tasklets():
    return render_template("list_tasklets.html",
                           tasklets=get_db()["tasklets"])


@app.route("/add/<int:priority>/<text>")
def add_tasklet(priority, text):
    get_db()["tasklets"].append(Tasklet(text, Priorities(priority)))
    return redirect(url_for("list_tasklets"))


@app.route("/done/<text>")
def mark_done(text):
    for tasklet in get_db()["tasklets"]:
        if tasklet.text == text:
            tasklet.done = True
            get_db().sync()
            return redirect(url_for("list_tasklets"))


if __name__ == '__main__':
    app.debug = True
    app.run()
