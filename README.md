# sqlalchemy-challenge

##Introduction

This project will analyze the climate in Honolulu, Hawaii, considering that a vacation is planned at this destination.

## Folders and files

* It is going to find a**folder** in this project:

   * The folder called `Resources` will find 2 CSV files ans 1 sqlite that were used to complete this challenge. Listed below are the names of the files you will find:

      * [hawaii.sqlite](https://github.com/ricardodelosrios/sqlalchemy-challenge/blob/main/Resources/hawaii.sqlite)
      * [hawaii_measurements.csv](https://github.com/ricardodelosrios/sqlalchemy-challenge/blob/main/Resources/hawaii_measurements.csv)
      * [hawaii_stations.csv](https://github.com/ricardodelosrios/sqlalchemy-challenge/blob/main/Resources/hawaii_stations.csv)
    
  * It will find **2 Files** in this project:
  
    * [climate_starter.ipynb](https://github.com/ricardodelosrios/sqlalchemy-challenge/blob/main/climate_starter.ipynb): In this file are the queries to analyze and explore the Climate Data..
    * [app.py](https://github.com/ricardodelosrios/sqlalchemy-challenge/blob/main/app.py):There is a py file where a Flask API was designed.
   
## Analyze and Explore the Climate Data

It was used the files (`climate_starter.ipynb` and `hawaii.sqlite`) to complete your climate analysis and data exploration.

To complete this part of the exercise, the `SQLAlchemy` module is used, which is part of a Python library that is used to work with relational databases in a more efficient and readable way. As you can see below:

```
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

```
Below you will find the explanation of the functions that were used from the sqlalchemy module.

* `automap_base`: This is a part of SQLAlchemy's Object Relational Mapping (ORM) system. It provides a way to automatically map database tables to Python classes.
* `Session`: The Session class is part of SQLAlchemy's ORM system as well. It represents a workspace for your database operations. You create a session when you want to interact with the database, and it keeps track of changes and transactions.
* `create_engine`: This function is used to create a database engine. The engine serves as the foundation for interacting with the database. It establishes a connection to the database and manages database connections and transactions.
* `func`: The func module allows you to use SQL functions in your SQLAlchemy queries. This is especially useful when you need to perform calculations or aggregate data within your queries.
* `inspect`: The inspect module is used to inspect database objects, such as tables, and gather information about them. It can be helpful when you need to dynamically query and analyze the database structure.

If you want to know more about SQLAlchemy you can use the following [documentation](https://docs.sqlalchemy.org/en/20/).






