import pytz
import sqlite3
import datetime


db = sqlite3.connect("c:\\Users\\13473\\OneDrive\\Documents\\Python Scripts\\check_in.db",
                     detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS employee (name TEXT PRIMARY KEY NOT NULL, "
           "check_in TIMESTAMP NOT NULL, check_out TIMESTAMP)")


class Employee:

    @staticmethod
    def _get_time_():
        return pytz.utc.localize(datetime.datetime.utcnow()).astimezone()

    def __init__(self, name: str):
        self.name = name

    def check_in(self):
        db.execute("INSERT INTO employee(name, check_in, check_out) VALUES (?, ?, ?)",
                   (self.name, int(datetime.datetime.utcnow().timestamp()), None))

    def check_out(self):
        db.execute("UPDATE employee SET check_out = ? WHERE name = ? AND check_out = ?",
                   (int(datetime.datetime.utcnow().timestamp()), self.name, None))

    def time_difference(self):
        cursor = db.execute("SELECT check_in, check_out FROM employee WHERE name=?", (self.name,))
        data = cursor.fetchone() # Data is (check_in, check_out) OR None.
        if data is None:
            return None
        else:
            if data[0] is not None and data[1] is not None:
                return data[1] - data[0]
            return None


if __name__ == '__main__':
    john = Employee("John")
