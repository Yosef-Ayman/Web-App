# Jobify

A modern job portal built with Django that connects job seekers with employers through a simple and user-friendly platform.

## Features

### Authentication & Accounts

* User registration and login
* Password reset functionality
* Role-based accounts

  * Job Seekers
  * Employers
* User onboarding process

### Job Seekers

* Browse available jobs
* View job details
* Apply for jobs
* Manage personal profile
* Track submitted applications

### Employers

* Create and manage company profile
* Post new job opportunities
* Edit existing jobs
* Delete job listings
* View applicants for each job
* Manage posted jobs through an employer dashboard

### Platform Pages

* Home page
* About page
* Contact page
* Help page
* Privacy Policy
* Terms & Conditions
* Custom error pages (400, 403, 404, 500)

## Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript
* Font Awesome

## Project Structure

```text
accounts/      Authentication, profiles, onboarding
jobs/          Job listings and applications
employers/     Employer dashboard and job management
static/        CSS, JavaScript, images
config/        Django project configuration
```

## Installation

### Clone the repository

```bash
git clone https://github.com/Yosef-Ayman/Web-App
cd Jobify
```

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Seed categories

```bash
python manage.py seed_categories
```

### Run development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

## Future Improvements

* Resume upload support
* Advanced job filtering
* Search functionality
* Email notifications
* Company verification
* REST API integration
* Admin analytics dashboard
