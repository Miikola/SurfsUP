import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///titanic.sqlite")
engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def date_prcp():
    # Query the dates and prcp observations from the last year
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= '2016-08-23').all()

    precip = {date: prcp for date, prcp in results}

    #Return the JSON represenation the dictionary
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def station_names():
    """Return a JSON list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stationID = list(np.ravel(results))

    return jsonify(stationID)

@app.route("/api/v1.0/tobs")
def date_tobs():
    # Query the dates and tobs observations from the last year
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date >= '2016-08-23').all()

    temps = {date: tobs for date, tobs in results}

    #Return the JSON represenation the dictionary
    return jsonify(temps)

@app.route("/api/v1.0/<startDate>")
def startResults(startDate):
# #     """Return a JSON list of minimum temperature, the average temperature and the max temperature for a given start range"""
# #     # Query all tobs of previous year

    startResults = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= '2016-08-23').all()

# #     # Convert list of tuples into normal list
#     all_start = list(np.ravel(start))
        
#     return jsonify(all_start)

# @app.route("/api/v1.0/<start>/<end>")
# # def start_end():
# #     ""Return a JSON list of minimum temperature, the average temperature and the max temperature for a given start-end range"""
#     start_end_list = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
#     filter(Measurement.date >= '2016-08-23').all()

# #     # Convert list of tuples into normal list
#     all_start_end = list(np.ravel(start_end_list))

#     return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True)