"""SQLite connection handling and schema initialization."""

import sqlite3

import click
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    total_stock INTEGER NOT NULL CHECK (total_stock >= 0),
    available_stock INTEGER NOT NULL CHECK (available_stock >= 0),
    CHECK (available_stock <= total_stock)
);

CREATE TABLE IF NOT EXISTS loan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL CHECK (length(trim(student_id)) > 0),
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status TEXT NOT NULL DEFAULT 'BORROWED'
        CHECK (status IN ('BORROWED', 'RETURNED', 'CANCELLED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES item (id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_loan_student_id ON loan (student_id);
"""


def get_db():
    """Return the request-scoped connection, creating it when necessary."""
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        # SQLite disables foreign keys per connection by default.
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(exception=None):
    """Close the request-scoped connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the tables if they do not exist yet."""
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


@click.command("init-db")
def init_db_command():
    """Create the SQLite tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database hooks and CLI commands on the application."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
