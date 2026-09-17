# crud-web-application
# CRUD Web Application

## Project Description

This project is a simple CRUD-based web application developed using Flask and SQLite. It allows users to create, view, update, and delete records through a user-friendly web interface.

## Technologies Used

* HTML
* CSS
* JavaScript
* Python
* Flask
* SQLite

## Features

* Create new records
* View existing records
* Update records
* Delete records
* Form validation
* Database storage
* Simple and responsive user interface

## CRUD Operations

| Operation | Method      | Purpose                   |
| --------- | ----------- | ------------------------- |
| Create    | POST        | Add a new record          |
| Read      | GET         | Display records           |
| Update    | PUT/POST    | Modify an existing record |
| Delete    | DELETE/POST | Remove a record           |

## Project Structure

```text
crud-web-application/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── database.db
├── requirements.txt
└── README.md
```

## How to Run

### Step 1: Install Python

Make sure Python is installed on your computer.

### Step 2: Install Flask

Open Command Prompt or Terminal and run:

```bash
pip install flask
```

### Step 3: Run the Application

Open the project folder and run:

```bash
python app.py
```

### Step 4: Open in Browser

Open:

```text
http://127.0.0.1:5000
```

## Database

SQLite is used as the database. It stores the records created through the application.

## Testing

The following operations were tested:

* Create record
* View record
* Update record
* Delete record
* Empty/invalid input validation

## Project Outcome

The application successfully demonstrates a complete CRUD workflow with frontend, backend, API, and database integration.

## Author

Name: Your Name
Department: Artificial Intelligence and Data Science
College: VSB College
Added complete CRUD web application
Added README documentation
