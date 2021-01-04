import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Creating the engine to SQLite database file 
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflecting existing database into a new modely 
Base = automap_base()

#Reflecting the tables. 
Base.prepare(engine, reflect=True)

#Saving a reference to the table 
measurement = Base.classes.measurement

station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """ Welcome to the Station Climate Home Page """
    return(
        f"""Available Routes:<br/><br/>
        
        
        /api/v1.0/precipitation<br/><br/>
        
        lists precipitation for last year of data<br/><br/>
        /api/v1.0/stations<br/><br/>
        
        lists all weather stations in Honolulu.<br/><br/>
        
        /api/v1.0/tobs<br/><br/>
        
        lists temperature observations for last year of data<br/><br/>
        
        /api/v1.0/&ltstart&gt<br/><br/>
        
        returns the MIN, AVG, and MAX temperature for<br/><br/>
        
        all dates greater than the start date<br/><br/>
        
        enter date as 'yyyy-mm-dd'.<br/><br/>
        
        /api/v1.0/&ltstart&gt/&ltend&gt<br/><br/>
        
        returns the MIN, AVG, and MAX temperature<br/><br/>
        
        for all dates between the start and end date<br/><br/>
        
        enter date as yyyy-mm-dd"""
    )

@app.route("/api/v1.0/precipitation")
def last_12_mth_prcp():
    
    #Calculates the desired date 
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_query = session.query(measurement.date,measurement.prcp).\
                        filter(measurement.date >= query_date).\
                        order_by(measurement.date).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    precip_json = [prcp_query]

    return jsonify(precip_json)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.name).all()
    stations_json = list(np.ravel(results))
    return jsonify(stations_json)

@app.route("/api/v1.0/tobs")
def temp_obs():
    #Calculates the desired date 
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    results = session.query(station.name, measurement.date, measurement.tobs).\
      filter(measurement.date >= query_date).all()
    tobs_json = list(np.ravel(results))
    return jsonify(tobs_json)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    results = session.query(measurement.date, func.avg(measurement.tobs), func.max(measurement.tobs),func.min(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    start_date_json = list(np.ravel(results))
    return jsonify(start_date_json)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):                   
    results = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >= start, measurement.date <= end).all()
    end_date_json = list(np.ravel(results))
    return jsonify(end_date_json)  


if __name__ == '__main__':
    app.run(debug=True)