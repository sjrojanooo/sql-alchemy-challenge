import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify

#################################################
# Database Setup
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
    """
    Welcome to the Station Climate Home Page
    """
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

    """
    Results of the 12 Month Percipitation analysis for all Stations
    """
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

if __name__ == "__main__":
    app.run(debug=True)
    