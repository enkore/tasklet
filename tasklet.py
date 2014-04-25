import re
import collections
from enum import Enum

from flask import Flask, g, redirect, url_for, render_template

DB_FILE = "tasklet"


class Priorities(Enum):
    green = 0
    blue = 1
    yellow = 2
    red = 3


class Tasklet:
    _text = ""
    priority = Priorities.green
    done = False

    def __init__(self, text):
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        markers = re.findall(":([a-zA-Z]+)", text)

        for marker in markers:
            if marker in Priorities.__members__:
                self.priority = Priorities[marker]
            if marker in ["done", "closed", "fixed", "resolved"]:
                self.done = True


class TaskletDB(collections.UserList):
    def __init__(self):
        super().__init__()

        with open(DB_FILE, "rb") as db_file:
            for line in db_file:
                self.append(Tasklet(line.decode("unicode_escape").strip()))

    def close(self):
        with open(DB_FILE, "wb") as db_file:
            for tasklet in self:
                db_file.write(tasklet.text.encode("unicode_escape"))
                db_file.write(b"\n")

app = Flask(__name__)


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        g._db = db = TaskletDB()
    return db


@app.route("/")
def list_tasklets():
    return render_template("list_tasklets.html",
                           tasklets=get_db())


@app.route("/add/<text>")
def add_tasklet(text):
    get_db().append(Tasklet(text))
    return redirect(url_for("list_tasklets"))


@app.route("/change/<text>/<new>")
def mark_done(text, new):
    for tasklet in get_db():
        if tasklet.text == text:
            tasklet.text = new
            return redirect(url_for("list_tasklets"))


if __name__ == '__main__':
    app.debug = True
    app.run()
