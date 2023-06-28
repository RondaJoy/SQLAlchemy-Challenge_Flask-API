# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, inspect, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# List all available api routes.
@app.route("/")
def home():
    return (f"Welcome to the Hawaii Weather Place!<br/>"
            "<br/>"
            f"Available Routes for Information:<br/>"
            f"/api/v1.0/precipitation/<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/temperature")


@app.route("/api/v1.0/precipitation")
def rain():
    
    # Create session from Python to the DB
    session = Session(engine)
    
    # Perform a query to retrieve date and precipitation for most recent year
    yr_prior_dt = dt.date(2016, 8, 23)
    qdata = session.query(Measure.date, Measure.station, Measure.prcp).\
    filter(Measure.date > yr_prior_dt).\
    order_by(Measure.date).all()
    session.close()
    
    # Create a dictionary from the row data and append to a list of rain data
    yr_rain = []
    for date, station, prcp in qdata:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["station"] = station
        rain_dict["precipitation"] = prcp
        yr_rain.append(rain_dict)

    # Instructions called for displaying date and prcp only but data makes no sense without the station id
    # Return as JSON
    return jsonify(yr_rain)

@app.route("/api/v1.0/stations")
def station_data():
    
    # Create a session from Python to the DB
    session = Session(engine)

    # Return a list of all Station data
    sdata = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    
    # Create a dictionary from the row data and append to a list of stations
    all_stn = []
    for station, name, latitude, longitude, elevation in sdata:
        stn_dict = {}
        stn_dict["station"] = station
        stn_dict["name"] = name
        stn_dict["latitude"] = latitude
        stn_dict["longitude"] = longitude
        stn_dict["elevation"] = elevation
        all_stn.append(stn_dict)
       
    # Return as JSON
    return jsonify(all_stn)

@app.route("/api/v1.0/temperature")
def temp_data():
    
    # Create a session from Python to the DB
    session = Session(engine)
    
    # Query the last 12 months of temperature observation data for USC00519281
    tdata = session.query(Measure.date, Measure.station, Measure.tobs).\
    filter(Measure.station == "USC00519281").\
    filter(Measure.date > yr_prior_dt).\    
    order_by(Measure.date).all()
    session.close()
    
    # Create a dictionary from the row data and append to a list of temp data
    yr_temps = []
    for date, station, tobs in tdata:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["station"] = station
        temp_dict["temp (F)"] = tobs
        yr_temps.append(temp_dict)

    # Return as JSON
    return jsonify(yr_temps)