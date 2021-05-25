from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import numpy as np
import pandas as pd

# Dictionary of Precipitation database set up 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes 
#################################################
app = Flask(__name__)

# create welcome route 

@app.route("/")
def welcome():
    return (
        f"Welcome to Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"

    )

# create precipitation route 

@app.route("/api/v1.0/precipitation")
def precipitation():
    """return precipitation date and precipitation scores"""
    # Calculate the date 1 year ago from the last data point in the database
    #Create our session (link) from Python to the DB
    session = Session(engine)

    # Use query from notebook. Get the last date in database, then calc a year before 
    last_date = session.query(func.max(Measurement.date)).first() 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # filter to one year ago 
    twelve_months_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()

    # create a list for results to jsonify 

    list_data = []
    for months in twelve_months_precip:
        data = {}
        data["date"] = months[0]
        data["prcp"] = months[1]
        list_data.append(data)

    #  jsonify the results 

    return jsonify(list_data)


# create stations route 

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all Stations"""

    results = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    #convert list of tuples to normal list 

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



# create tobs route 

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return dates and temparature observations for most active station for the last year of data"""
    # create a query to find temparature observations for most active station for the last year of data
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    twelve_months_obvs = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date >= year_ago) & (Measurement.station == "USC00519281")).all()

    session.close()

    tobs_obs = list(np.ravel(twelve_months_obvs))

    return jsonify(tobs_obs)



# create start date route 

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date"""

# query the min, max and average tobs 

    recorded_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs).filter(Measurement.date >= start)).all() 

    session.close()

#   create a list for results 

    temps_list = []
    for temp in recorded_temps:
        calcs = {}
        calcs["min"] = temp[0]
        calcs["max"] = temp[1]
        calcs["avg"] = temp[2]
        temps_list.append(calcs)


    return jsonify(temps_list)



if __name__ == "__main__":
    app.run(debug=True)
