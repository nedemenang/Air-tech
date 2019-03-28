# AIRTECH

## Project Description

Company Airtech has had their challenges using spreadsheets to manage their flight booking system. They are ready to automate their processes with an application and have reached out to you to build a flight booking application for the company.

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

On the prompt execute the following

```export $(cat .env```)

Execute the following code to install all the application dependencies.

```python install -r requirements.txt```

Execute the following code to migrate all data tables/object

```python run.py db migrate```

Execute the following code to seed the database

```flask seed_database```

Execute the following at the command line

```python run.py runserver```

Browse the application in the url

```http://localhost:5000/api/v1/```