# Flight Booker

[![Build Status](https://travis-ci.com/otseobande/flight-booker.svg?branch=master)](https://travis-ci.com/otseobande/flight-booker) [![codecov](https://codecov.io/gh/otseobande/flight-booker/branch/master/graph/badge.svg)](https://codecov.io/gh/otseobande/flight-booker)

## Features

- User registration
- User login
- Create flights
- Get flights
- Book a flight
- Get flight bookings

## Setup

- Install virtualenv

```bash
pip install virtualenv
```

- Create the application's virtual environment

```bash
virtualenv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate
```

- Setup environment variables

  Create a `.env` file, copy the content of the `.env.example` file into it and fill the necessary credentials

- Install dependencies

```bash
pip install -r requirements.txt
```

- Start the development server

```bash
python manage.py run_server
```

### Testing

Run `python manage.py test` to run tests

#### Performance monitoring

To test application performance run

```bash
locust --host=<application-host>
```

## Technologies Used

- [Flask](http://flask.pocoo.org/)
- [MongoDB](https://www.mongodb.com/)


## Documentation

- [API Documentation](https://documenter.getpostman.com/view/3424044/S1a4Y7Yo?version=latest#ea2cb554-596b-4939-a55c-60a23c9bcb71)

## Project Management

[Pivotal Tracker](https://www.pivotaltracker.com) is used for this project. You can find the management board [here](https://www.pivotaltracker.com/n/projects/2358405)
