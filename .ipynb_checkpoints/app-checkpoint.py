import sqlalchemy
import datetime as dt 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd 

from flask import Flask, jsonify

app = Flask(__name__)

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
    prcp_query = session.query(measurement.id,
                          measurement.station,
                          measurement.date,
                          measurement.prcp,
                          measurement.tobs).\
            filter(measurement.date >= query_date).\
            order_by(measurement.date).all()
    
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
def tstart(start):
    """ When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    results=session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= start).order_by(measurement.date.desc()).all()
    #list = []
    print(f"Temperature Analysis for the dates greater than or equal to the start date")
    for temps in results:
        dict = {"Minimum Temp":results[0][0],
                "Average Temp":results[0][1],
                "Maximum Temp":results[0][2]}
        #list.append(dict)
    return jsonify(dict) 

@app.route("/api/v1.0/<start>/<end>")
def tstartend(start,end):         
    """ When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive. """    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
                  filter(measurement.date >= start, measurement.date <= end).order_by(measurement.date.desc()).all()
    
    print(f"Temperature Analysis for the dates greater than or equal to the start date and lesser than or equal to the end date")
    
    for temps in results:
        
        dict = {"Minimum Temp":results[0][0],
                "Average Temp":results[0][1],
                "Maximum Temp":results[0][2]}
        
    return jsonify(dict)

if __name__ == "__main__":
    app.run(debug=True)
    