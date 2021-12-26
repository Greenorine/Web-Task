from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def dashboard():
    with get_db_connection() as con:
        res = list(con.execute("SELECT COUNT(*) as 'count', strftime('%Y', dateModify) as 'year' "
                           "FROM works WHERE year IS NOT NULL GROUP BY year"))
    data = [r["count"] for r in res]
    labels = [r["year"] for r in res]
    return render_template('year.html', cvs=res, data=data, labels=labels)


@app.route("/managers")
def managers():
    with get_db_connection() as con:
        res = list(con.execute(get_jobs_query(("manager", "менеджер"))))
    con.close()
    data = [r["count"] for r in res]
    labels = [r["qualification"] for r in res]
    return render_template('jobs.html', cvs=res, data=data, labels=labels, ql="менеджеров")


@app.route("/engineers")
def engineers():
    with get_db_connection() as con:
        res = list(con.execute(get_jobs_query(("engineer", "инженер"))))
    con.close()
    data = [r["count"] for r in res]
    labels = [r["qualification"] for r in res]
    return render_template('jobs.html', cvs=res, data=data, labels=labels, ql="инженеров")


def get_jobs_query(job_titles: tuple[str, str], count: int = 15):
    query = (f"SELECT LOWER(qualification) as 'qualification', count(*) as 'count' FROM works "
             f"WHERE qualification IS NOT NULL AND "
             f"(LOWER(jobTitle) like '%{job_titles[0]}%' OR LOWER(jobTitle) like '%{job_titles[1]}%')"
             f"GROUP BY LOWER(qualification) "
             f"ORDER BY count DESC LIMIT {count}")
    return query


def get_db_connection():
    con = sqlite3.connect('works.sqlite')
    con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    return con


app.run()
