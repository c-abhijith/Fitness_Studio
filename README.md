# Fitness Studio Booking


## About Project
This project is a Fitness Studio Booking system designed for two types of users: User and Instructor. The Instructor can create fitness classes based on specific dates and times. Users can book any class across different time zones. However, if an instructor has already scheduled a fitness class for a particular time slot, they cannot create another class that overlaps with that time. Similarly, if a user has booked a class at a specific time, they cannot book another class that conflicts with that same time slot. using technology  RESTful API built with Django REST Framework

## Features
- Authentication
- Permissions management
- Booking functionality
- Time zone support
- User-friendly interface for scheduling fitness sessions

## Technologies 
    - Django
    - DRF
    - SQLlite
    - simple JWT
    - Docker
    - black

## Setup Instructions

### windows
    python -m venv venv 
    venv\Scripts\activate
    pip install -r requirements.txt

    python manage.py makemigrations 

    python manage.py migrate       

    python manage.py runserver```



### Macos / Linux
    python -m venv venv
    source venv/bin/activate

    make run-local```

## Docker
    docker-compose --build
    docker-compose up ```



Create a virtual environment and install the dependencies. The SQLite database for this project is saved locally in the project directory, and the database password is TheGod@123. Permissions are set up to manage different user roles effectively.



### password : TheGod@123