# Fusion Application


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Run](#run-without-docker)
- [Usage](#usage)
- [API Documentation](#api-documentation)


## Prerequisites

Before you begin, ensure you have met the following requirements:

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git@github.com:zahid10cse/django-sample.git
   ```

2. Navigate to the project directory:
    ```bash
    cd django-sample
    ```

3. Once environment variable are set run below command
    ```bash
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

   ### Create User
   Open terminal and run below command to Run the test:
   
   ```bash
    python manage.py createsuperuser
   ```

## Usage

1. Access the application in your web browser:
    ```
    http://localhost:8000
    ```

## API Documentation
   ```bash
    http://localhost:8000/docs/
   ```
