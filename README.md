# Fitness Studio Booking

This project is a Fitness Studio Booking system.

## Features
- Authentication
- Permissions management
- Booking functionality
- Time zone support
- User-friendly interface for scheduling fitness sessions

## Setup Instructions

### windows
    ```bash
    python -m venv venv 
    venv\Scripts\activate
    pip install -r requirements.txt

    python manage.py makemigrations --> no need to do, already done

    python manage.py migrate        --> no need to do , already done

    python manage.py runserver




### Macos / Linux
    python -m venv venv
    source venv/bin/activate

    make run-local


## Docker
    docker-compose --build
    docker



Create a virtual environment:


