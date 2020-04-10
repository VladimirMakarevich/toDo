import sqlite3

from flask import Flask

app = Flask(__name__)


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()
        # Why are we calling user table before to_do table
        # what happens if we swap them?

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Todo (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done boolean DEFAULT 0,
          _is_deleted boolean DEFAULT 0,
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """

        self.conn.execute(query)
        self.conn.commit()

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS User (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT,
        CreatedOn Date default CURRENT_DATE
        );
        """

        self.conn.execute(query)
        self.conn.commit()


class ToDoModel:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, id: int):
        where_clause = " AND id=" + str(id) + ""
        return self.list_items(where_clause)

    def create(self, params):
        print(params)
        query = "insert into Todo (Title, Description, DueDate, UserId) values ('" + params.get("Title") + \
                "', '" + params.get("Description") + "', '" + params.get("DueDate") + "', '" + params.get("UserId") + \
                "')"
        app.logger.info(query)
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id: int):
        query = "UPDATE " + "Todo" + \
                "SET _is_deleted = 1 " + \
                "WHERE id = " + str(item_id)
        print(query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, item_id: int, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = " ".join([column + "=" + value
                              for column, value in update_dict.items()])

        query = "UPDATE " + "Todo" + \
                "SET " + set_query + \
                "WHERE id = " + str(item_id)
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = "SELECT id, Title, Description, DueDate, _is_done " + \
                "from Todo WHERE _is_deleted != 1 " + where_clause
        print(query)
        app.logger.info(query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class User:

    def create(self, name: str, email: str):
        query = 'insert into ' + 'User' + \
                '(Name, Email) ' + \
                'values (' + name + email + ')'
        result = self.conn.execute(query)
        return result
