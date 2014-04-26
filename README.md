
# Tasklet

Tasklet is a very simple and basic, browser-based todo list / task manager.

It doesn't have anything like user accounts, authentication and
doesn't need a database. It's meant to be run local, on your personal
machine. It doesn't sync with the cloud or your phone. You can add
to-do items by `echo`ing to ~/.tasklet. You can distribute/rsync/git
your ~/.tasklet to synchronize todo lists.

It stores items ("tasklets") by default in a text file (`~/.tasklet`), one item per line.

It supports assigning items to four different priorities/colors:

* :green (default)
* :blue
* :yellow
* :red

Likewise items are marked done by adding `:done` (or any other of
`DONE_WORDS`, see tasklet.py).  Items are deleted by using one of
DELETE_WORDS.

Edit items by double-clicking them. Hit enter when done editing,
changes are saved instantly. Click the X or use DELETE_WORDS to delete an item.

Add items by writing something into the input line at the top of the
page.

Quickly search items by typing into the input line without pressing enter.

Drag and drop items to rearrange.

## "Deployment"

If you have flask already installed, just execute tasklet.py to run
it. By default it runs on http://127.0.0.1:7123/

If not run `pip install -r requirements.txt`.

## Dependencies

- Python 3
- Flask
