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

# Create our session (link) from Python to the DB
# session = Session(engine)


#################################################
# Flask Routes 
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> "
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    """return precipitation date and precipitation scores"""
    # Calculate the date 1 year ago from the last data point in the database
    #Create our session (link) from Python to the DB
    session = Session(engine)
    last_date = session.query(func.max(Measurement.date)).first()
        
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    twelve_months_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()

    # create a dictionary with date as key, precip as value 
    precip_12 = {date: precip for date, precip in twelve_months_precip}

    return jsonify(precip_12)



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



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and temparature observations for most active station for the last year of data"""
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    twelve_months_obvs = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date >= year_ago) & (Measurement.station == "USC00519281")).all()

    session.close()

    tobs_obs = list(np.ravel(twelve_months_obvs))

    return jsonify(tobs_obs)


@app.route("/api/v1.0/<start>")
def start_date():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date"""
    sel = [Measurement.date, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
    recorded_temps = session.query(*sel).filter(Measurement.date >= <start>).all()
# print the results


    session.close()

    for temp in recorded_temps:
        print()

    start_retult = list(np.ravel(recorded_temps))


    return jsonify(start_retult)



# @app.route("/api/v1.0/<start>/<end>")




if __name__ == "__main__":
    app.run(debug=True)
