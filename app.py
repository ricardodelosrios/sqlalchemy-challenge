# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

Measurement= Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB

session=Session(bind=engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """Server received request for 'Home' page..."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all precipitation"""
    ## Find the most recent date in the data set.
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    last_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    print(last_date)
    
    # Perform a query to retrieve the data and precipitation scores
    data_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).order_by(Measurement.date).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    df = pd.DataFrame(data_prcp, columns=['Date', 'Inches'])

    df1=df.dropna(how="any")
    
    # Sort the dataframe by date
    
    df_sorted =df1.sort_values(by="Date")
   
    session.close()

    # Create a dictionary 

    precipitation_dictionary = []
    for index, row in df_sorted.iterrows():
        precipitation_dict = {}
        precipitation_dict["Date"] = row['Date']
        precipitation_dict["Inches"] = row['Inches']
        precipitation_dictionary.append(precipitation_dict)

    #Return the JSON representation of your dictionary.
    return jsonify(precipitation_dictionary) 
   
  


@app.route("/api/v1.0/stations")
def station():

    # Return a JSON list of stations from the dataset.
    
    """Return a list of all stations"""
    
    hawaii_stations_path = "Resources/hawaii_stations.csv"

    # Read files
    
    hawaii_stations = pd.read_csv(hawaii_stations_path)

    # Display the data table for preview 

    station_list = pd.DataFrame(hawaii_stations, columns=['station','name'])
    
    # Convert DataFrame rows to JSON using a for loop

    station_json = []
    for index, row in station_list.iterrows():
        json_data = {
            'station': row['station'],
            'name': row['name']
        }
        station_json.append(json_data)
  
    return (station_json) 


@app.route("/api/v1.0/tobs")
def temperature():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all temperature observations"""
    
    ## Find the most recent date in the data set.
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    last_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    print(last_date)
    
    # List the stations and their counts in descending order.
    act_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    twelve_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == act_stations[0].station).filter(Measurement.date >= last_date)

    session.close()


    #Return a JSON list of temperature observations for the previous year

    tobs_json = []
    for row in twelve_temps:
        json_data = {
            'tobs': row['tobs']
        }
        tobs_json.append(json_data)
  
    return (tobs_json) 


@app.route("/api/v1.0/<start>")
def average(start):

    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

    hawaii_measurements_path = "Resources/hawaii_measurements.csv"

    # Read files    
    hawaii_measurements = pd.read_csv(hawaii_measurements_path)

    # Finds specific date in the dataset 
    tem_start = pd.DataFrame(hawaii_measurements, columns=['date', 'tobs']).query("date == @start")
    if (not tem_start.empty):
        summary_stats = tem_start.agg({'tobs': ['min', 'mean', 'max']})
        return summary_stats.to_json()
    return jsonify({"error": f"Date {start} not found."}), 404


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):


    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

    hawaii_measurements_path = "Resources/hawaii_measurements.csv"

    # Read files    
    hawaii_measurements = pd.read_csv(hawaii_measurements_path)

    # Finds data for specific range between start date and end date in the dataset 
  
    tem_start = pd.DataFrame(hawaii_measurements, columns=['date', 'tobs']).query("date > @start and date <= @end")

    # return temp_start.to_json()

    if (not tem_start.empty):
        summary_stats = tem_start.agg({'tobs': ['min', 'mean', 'max']})
        return summary_stats.to_json()
    return jsonify({"error": f"Date {start, end} not found."}), 404
    

if __name__ == '__main__':
    app.run(debug=True)