import os.path, re, collections, enum

from flask import Flask, g, redirect, url_for, render_template, request, abort

DB_FILE = "~/.tasklet"
DONE_WORDS = ["done", "closed", "fixed", "resolved"]
DELETE_WORDS = ["rm", "remove", "del", "delete"]

DB_FILE = os.path.expandvars(os.path.expanduser(DB_FILE))
app = Flask(__name__)


class Priorities(enum.Enum):
    green = 0
    blue = 1
    yellow = 2
    red = 3


class Tasklet:
    _text = ""
    priority = Priorities.green
    done = False
    delete = False

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
            if marker in DONE_WORDS:
                self.done = True
            if marker in DELETE_WORDS:
                self.delete = True


class TaskletDB(collections.UserList):
    def __init__(self):
        super().__init__()

        with open(DB_FILE, "rb") as db_file:
            for line in db_file:
                self.append(Tasklet(line.decode("unicode_escape").strip()))

    def close(self):
        with open(DB_FILE, "wb") as db_file:
            for tasklet in self:
                if tasklet.delete:
                    continue
                db_file.write(tasklet.text.encode("unicode_escape"))
                db_file.write(b"\n")


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


@app.route("/add/", methods=["POST"])
def add_tasklet():
    if "text" not in request.form:
        abort(400)
    get_db().insert(0, Tasklet(request.form["text"]))
    return "added"


@app.route("/change/", methods=["POST"])
def change():
    if "text" in request.form and "new" in request.form:
        for tasklet in get_db():
            if tasklet.text == request.form["text"]:
                tasklet.text = request.form["new"]
                return "changed"
    abort(400)


@app.route("/move/", methods=["POST"])
def move():
    if "text" in request.form and "pos" in request.form:
        pos = int(request.form["pos"])
        for i, tasklet in enumerate(get_db()):
            if tasklet.text == request.form["text"]:
                break
        else:
            abort(404)
        get_db().data = get_db()[:i] + get_db()[i+1:]
        get_db().insert(pos+1, tasklet)
        return "moved"
    abort(400)


if __name__ == '__main__':
    app.run(port=7123, host="127.0.0.1")
