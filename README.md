[![Coverage Status](https://coveralls.io/repos/github/nedemenang/Air-tech/badge.svg?branch=master)](https://coveralls.io/github/nedemenang/Air-tech?branch=master)  [![Build Status](https://travis-ci.org/nedemenang/Air-tech.svg?branch=master)](https://travis-ci.org/nedemenang/Air-tech)



# AIRTECH

## Project Description

Company Airtech has had their challenges using spreadsheets to manage their flight booking system. They are ready to automate their processes with an automatic flight booking application for the company.

The flight booking system provides an API that enables the users to:

*   Log in
*   Upload passport photographs
*   Book tickets
*   Receive tickets as an email
*   Check the status of their flight
*   Make flight reservations
*   Purchase tickets

The flight booking system is also able to:

*   Encrypt password
*   Handle multiple requests
*   Optimize via caching and multithreading

# Usage
Using Python download and install version of Python 3.7

The application is built with Python

To clone the respository execute the following command.

```git clone https://github.com/andela/airtech.git```

Navigate into the cloned project directory.

Edit the env-sample file with your credentials and save it as .env. Change the parameters in there to your own settings.

The key FLASK_APP must be set to run.py. The value of the APP_ENV between development and testing in order to run the application in development or testing mode respectively.

## Setting up a virtual environment
Run: `virtualenv venv --python=python3.7` in project directory to install a python3.7 virtual environment

Run: `source venv/bin/activate` to activate virtual environment

On the prompt execute the following

```export $(cat .env)```

Execute the following code to install all the application dependencies.

```python install -r requirements.txt```

Execute the following code to migrate all data tables/object

```python run.py db migrate```

Execute the following code to seed the database

```python run.py seed_all```

Execute the following at the command line

```python run.py runserver```

Browse the application in the url

```http://localhost:5000/api/v1/```