Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Tech Stack

Includes:

* **SQLAlchemy ORM**
* **PostgreSQL**
* **Python 3**
* **Flask**
* **Flask-Migrate**
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) 

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. "python app.py" to run after installing dependences
  ├── models.py  *** SQLAlchemy models.               
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── enums.py
  ├── forms.py ***
  ├── requirements.txt *** The dependencies needed to be installed with "pip install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```


### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask).

  ```
  $ cd ~
  $ sudo pip install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ python -m venv env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

### Motivation

This project was completed as part of the Full Stack Developer Nanodegree Program. Which I took to broaded my skill set on the back end.