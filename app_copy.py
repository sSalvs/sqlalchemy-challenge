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

@app.route("/api/v1.0/precipitation")
def precipitation():
    """return precipitation for three years"""
    # Calculate the date 1 year ago from the last data point in the database

    last_date = session.query(func.max(Measurement.date)).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    twelve_months_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # create a dictionary with date as key, precip as value 
    precip_12 = {date: precip for date, precip in twelve_months_precip}



    return jsonify(precip_12)


@app.route("/")
def welcome():
    return (
        f"Welcome to Climate Change!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> "
    )


if __name__ == "__main__":
    app.run(debug=True)
