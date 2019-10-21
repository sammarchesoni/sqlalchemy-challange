import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> - (YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> - (YYYY-MM-DD)<br/>"
    )

# Precipication
sel = [Measurement.date, Measurement.prcp]
date = dt.datetime(2016,8,23)
end_date1 = dt.datetime(2017,8,23)
precipitation = session.query(*sel).filter(Measurement.date >= date).order_by(Measurement.date).all()
prec_dict = []
for n in precipitation:
    row = {}
    row["date"] = precipitation[0]
    row["prcp"] = precipitation[1]
    prec_dict.append(row)
@app.route("/api/v1.0/precipitation")
def rainfall():
    print("Server received request for 'Precipitation' page...")
    return jsonify(prec_dict)

# Stations
station = session.query(Station.name, Station.station).all()
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    return jsonify(station)

# TOBS
temp = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= date).order_by(Measurement.date).all()
@app.route("/api/v1.0/tobs")
def temperature():
    print("Server received request for 'tobs' page...")
    return jsonify(temp)

# <start>
@app.route("/api/v1.0/<start>")
def calc_temps(start):
    session = Session(engine)
    start = start.replace(" ","")
    pleasework = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()    
    return jsonify(pleasework)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_end(start,end):
    session = Session(engine)
    start = start.replace(" ","")
    pleasework = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()    
    return jsonify(pleasework)

if __name__ == "__main__":
    app.run(debug=True)
