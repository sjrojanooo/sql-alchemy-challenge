# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/Hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

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
def home():
    """ Welcome to the Station Climate Home Page """
    return(
        f"""Available Routes:<br/><br/>
        
        
        api/v1.0/precipitation<br/>
        
        lists precipitation for last year of data<br/><br/>
        /api/v1.0/stations<br/>
        
        lists all weather stations in Honolulu.<br/><br/>
        
        /api/v1.0/tobs<br/>
        
        lists temperature observations for last year of data<br/><br/>
        
        /api/v1.0/&ltstart&gt<br/>
        
        returns the MIN, AVG, and MAX temperature for<br/><br/>
        
        all dates greater than the start date<br/>
        
        enter date as 'yyyy-mm-dd'.<br/><br/>
        
        /api/v1.0/&ltstart&gt/&ltend&gt<br/><br/>
        
        returns the MIN, AVG, and MAX temperature<br/>
        
        for all dates between the start and end date<br/>
        
        enter date as 'yyyy-mm-dd'<br/>"""
    )

@app.route("/api/v1.0/precipitation")
def percipitation():

    """ Results of the 12 Month Percipitation analysis for all Stations """
    prcp_query = session.query(measurement.date, func.avg(measurement.prcp)).\
    filter(measurement.date>='2016-08-23').group_by(measurement.date).all()
    
    #Create a list of dicts with 'date' as they key and 'prcp' as the value
    precipitation = []
    
    for result in prcp_query:
        
        row = {}
        
        row["date"] = result[0]
        
        row["total"] = float(result[1])
        
        precipitation.append(row)
        
    #Jsonify results
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """ Returning the all Stations """
    station_list = session.query(station.name).all()
    
    jsonify_sation = list(np.ravel(station_list))
    
    #Jsonify results 
    return jsonify(jsonify_sation)

@app.route("/api/v1.0/tobs")
def tobs():
    """ Return a JSON list of Temperature Observations (tobs) for the previous year."""  
    Range = date_calc()
    End_date = Range[1]
    Start_date = Range[0]
    tobs = session.query(measurement.date,measurement.tobs).\
                            filter(measurement.date <= End_date).\
                            filter(measurement.date >= Start_date).all()
    list = []
    for temp in tobs:
        dict = {"date": temp[0], "tobs": temp[1]}
        list.append(dict)

    return jsonify(list) 


@app.route("/api/v1.0/<start>")
def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)



if __name__ == "__main__":
    app.run(debug=True)