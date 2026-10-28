from flask import Flask, render_template, request, jsonify
import sqlite3, csv, os, random
from datetime import datetime

app = Flask(__name__)
DB = "crime.db"

CRIME_TYPES = ["Theft", "Robbery", "Burglary", "Assault", "Cybercrime", "Other"]
AREAS = ["Chunabhatti", "Sion", "Chembur", "Kurla", "Vashi", "Sanpada"]

def init_db():
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS crimes(
        id INTEGER PRIMARY KEY, crime_type TEXT, area TEXT, date TEXT,
        time TEXT, latitude REAL, longitude REAL, risk TEXT, description TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS concerns(
        id INTEGER PRIMARY KEY, area TEXT, date_time TEXT, concern TEXT,
        description TEXT, photo TEXT)""")
    cur.execute("SELECT COUNT(*) FROM crimes")
    if cur.fetchone()[0] == 0:
        random.seed(7)
        samples=[]
        coords={
            "Chunabhatti":(19.0522,72.8840),"Sion":(19.0460,72.8630),
            "Chembur":(19.0620,72.8970),"Kurla":(19.0726,72.8845),
            "Vashi":(19.0757,72.9977),"Sanpada":(19.0676,73.0090)
        }
        for i in range(120):
            area=random.choice(AREAS)
            typ=random.choice(CRIME_TYPES)
            hour=random.choice(list(range(0,24)))
            risk="High" if hour in list(range(21,24))+list(range(0,5)) else ("Medium" if hour in [7,8,18,19,20] else "Low")
            lat,lon=coords[area]
            samples.append((typ,area,f"2026-{random.randint(1,9):02d}-{random.randint(1,28):02d}",
                            f"{hour:02d}:{random.randint(0,59):02d}",lat+random.uniform(-.004,.004),
                            lon+random.uniform(-.004,.004),risk,"Sample academic dataset"))
        cur.executemany("""INSERT INTO crimes(crime_type,area,date,time,latitude,longitude,risk,description)
                           VALUES(?,?,?,?,?,?,?,?)""",samples)
    con.commit(); con.close()

def query(sql,args=()):
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
    rows=con.execute(sql,args).fetchall(); con.close()
    return rows

@app.route("/")
def home():
    total=query("SELECT COUNT(*) c FROM crimes")[0]["c"]
    return render_template("index.html", total=total)

@app.route("/dashboard")
def dashboard():
    total=query("SELECT COUNT(*) c FROM crimes")[0]["c"]
    types=query("SELECT crime_type name, COUNT(*) value FROM crimes GROUP BY crime_type ORDER BY value DESC")
    areas=query("SELECT area name, COUNT(*) value FROM crimes GROUP BY area ORDER BY value DESC")
    months=query("SELECT substr(date,1,7) name, COUNT(*) value FROM crimes GROUP BY name ORDER BY name")
    return render_template("dashboard.html",total=total,types=[dict(x) for x in types],
                           areas=[dict(x) for x in areas],months=[dict(x) for x in months])

@app.route("/map")
def crime_map():
    points=query("SELECT id,crime_type,area,date,time,latitude,longitude,risk FROM crimes")
    return render_template("map.html", points=[dict(x) for x in points])

@app.route("/geo")
def geo(): return render_template("geo.html")

@app.route("/crime-info")
def crime_info(): return render_template("crime_info.html")

@app.route("/safety")
def safety(): return render_template("safety.html")

@app.route("/survey")
def survey(): return render_template("survey.html")

@app.route("/results")
def results(): return render_template("results.html")

@app.route("/findings")
def findings():
    top=query("SELECT crime_type,COUNT(*) n FROM crimes GROUP BY crime_type ORDER BY n DESC LIMIT 1")[0]
    area=query("SELECT area,COUNT(*) n FROM crimes GROUP BY area ORDER BY n DESC LIMIT 1")[0]
    return render_template("findings.html",top=dict(top),area=dict(area))

@app.route("/risk", methods=["GET","POST"])
def risk():
    result=None
    if request.method=="POST":
        area=request.form.get("area")
        typ=request.form.get("crime_type")
        time=request.form.get("time","12:00")
        h=int(time.split(":")[0])
        score=0
        if area in ["Chunabhatti","Kurla"]: score+=1
        if typ in ["Robbery","Burglary","Assault"]: score+=2
        if h>=21 or h<5: score+=2
        elif h in [7,8,18,19,20]: score+=1
        result="High" if score>=4 else ("Medium" if score>=2 else "Low")
    return render_template("risk.html",result=result,areas=AREAS,types=CRIME_TYPES)

@app.route("/report", methods=["GET","POST"])
def report():
    msg=None
    if request.method=="POST":
        con=sqlite3.connect(DB)
        con.execute("INSERT INTO concerns(area,date_time,concern,description,photo) VALUES(?,?,?,?,?)",
                    (request.form["area"],request.form["date_time"],request.form["concern"],
                     request.form["description"],request.form.get("photo","")))
        con.commit(); con.close(); msg="Safety concern submitted successfully."
    return render_template("report.html",msg=msg)

@app.route("/emergency")
def emergency(): return render_template("emergency.html")

@app.route("/methodology")
def methodology(): return render_template("methodology.html")

@app.route("/dataset")
def dataset():
    rows=query("SELECT * FROM crimes LIMIT 100")
    return render_template("dataset.html",rows=[dict(x) for x in rows])

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/references")
def references(): return render_template("references.html")

@app.route("/api/crimes")
def api_crimes():
    return jsonify([dict(x) for x in query("SELECT * FROM crimes")])

if __name__=="__main__":
    init_db()
    app.run(host='0.0.0.0', port=10000)
