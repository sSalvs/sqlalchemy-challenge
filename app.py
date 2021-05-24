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
    """return precipitation date and precipitation scores"""
    # Calculate the date 1 year ago from the last data point in the database
    #Create our session (link) from Python to the DB
    session = Session(engine)
    last_date = session.query(func.max(Measurement.date)).first()
    
    session.close()

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    twelve_months_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # create a dictionary with date as key, precip as value 
    precip_12 = {date: precip for date, precip in twelve_months_precip}



    return jsonify(precip_12)




@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all Stations"""

    results = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    #convert list of tuples to normal list 

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and temparature observations for most active station"""
    
    twelve_months_obvs = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date >= year_ago) & (Measurement.station == "USC00519281")).all()

    session.close()

    tobs_obs = list(np.ravel(twelve_months_obvs ))

    return jsonify(tobs_obs)


@app.route("/api/v1.0/<start>")



@app.route("/api/v1.0/<start>/<end>")


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
