import pytz
import sqlite3
import datetime


db = sqlite3.connect("c:\\Users\\13473\\Documents\\Python Scripts\\check_in.db",
                     detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS report_in (_id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
           "check_in TIMESTAMP NOT NULL, date TIMESTAMP NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS report_out (_id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
           "check_out TIMESTAMP NOT NULL, date TIMESTAMP NOT NULL)")

month = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


class Employee:

    @staticmethod
    def _get_time_():
        return pytz.utc.localize(datetime.datetime.utcnow()).astimezone()

    def __init__(self, name: str):
        self.name = name

    def check_in(self):
        db.execute("INSERT INTO report_in (name, check_in, date) VALUES (?, ?, ?)",
                   (self.name, self._get_time_(), datetime.date.today()))
        db.commit()

    def check_out(self):
        db.execute("INSERT INTO report_out (name, check_out, date) VALUES (?, ?, ?)",
                   (self.name, self._get_time_(), datetime.date.today()))
        db.commit()

    def time_accumulation(self):
        period = self._get_time_().month
        cursor = db.cursor()
        cursor.execute("SELECT check_in, check_out FROM report_in JOIN report_out "
                       " ON report_in._id = report_out._id"
                       " WHERE report_in.name = ? ORDER BY report_in._id"
                       " AND strftime('%m', report_in.date = ?)", (self.name, period))
        data = cursor.fetchall()
        accumulation = []
        for check_in, check_out in data:
            lapse = check_out - check_in
            accumulation.append(float(lapse.total_seconds()))
        return sum(accumulation) // 3600

    def __str__(self):
        x = self._get_time_().month
        y = self.time_accumulation()
        return "{0.name} worked {1} hours in {2}.".format(self, y, month.get(x))


if __name__ == '__main__':
    # TESTING
    john = Employee("John")
    john.check_in()
    john.check_out()
    john.time_accumulation()
    print(john)

db.close()

