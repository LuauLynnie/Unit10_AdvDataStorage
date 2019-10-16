# Surfs Up / app.py
from flask import Flask, jsonify
# Dependencies
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm  import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurements
Stations = Base.classes.stations

session = Session(engine)

@app.route("/")
def home():
    print("Server received request for 'Home' page.")
    return "Welcome to the Surfs Up Weather API"

@app.route("/welcome")
# List all available routes
def welcome ():
    return (
        f"Welcome to the Surfs Up API<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurements.date,Measurements.prcp).filter(Measurements.date >= "04-08-2017").all()
    
    year_prcp = list(np.ravel(results))
    # Results.__dict__
    # Create a dictionary using 'date' as the key and 'prcp' as the value.
    """year_prcp = []
    for result in results:
            row = {}
            row[Measurements.date] = row[Measurements.prcp]
            year_prcp.append(row)"""
    
    return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Return a json list of stations from the dataset.
    results = session.query(Stations.station).all()
    
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    # Return a json list of temperature Observations (tobs) for the previous year.
    years_tobs = []
    results = session.query(Measurements.tobs).filter(Measurements.date >= "04-08-2017").all()
    
    years_tobs = list(np.ravel(results))
    
    return jsonify(year_tobs)

@app.route("/api/v1.0/<start>")
def start_trip_temp(start_date):
    start_trip = []
    
    results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date == start_date).all()
    results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date == start_date).all()
    results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date == start_date).all()
    
    start_trip = list(np.ravel(results_min,results_max, results_avg))
    
    return jsonify(start_trip)

def greater_start_date(start_date):
    
    start_trip_date_temps = []
    
    results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    
    start_trip_date_temps = list(no.ravel(results_min,results_max, results_avg))
    
    return jsonify(start_trip_date_temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end_trip(start_date, end_date):
    
    start_end_trip_temps = []
    
    results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date == start_date, Measurements.date == end_date).all()
    results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date == start_date, Measurements.date == end_date).all()
    results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date == start_date, Measurements.date == end_date).all()
    
    start_end_trip_temps = list(np.ravel(results_min,results_max, results_avg))
    
    return jsonify(start_trip_date_temps)

def start_end_trip(start_date, end_date):
    
    round_trip_temps = []
    
    results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
    results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
    results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
    
    round_trip_temps = list(np.ravel(results_min,results_max, results_avg))
    
    return jsonify(round_trip_temps)


if __name__ == '__main__':
    app.run(debug=True)
    



        
        
        
        
        
        
        
        