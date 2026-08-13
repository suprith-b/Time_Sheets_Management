# TimeSheets Management

TimeSheets Management is a time-tracking and reporting application that allows employees to log their working hours and provides role-based access to manage employees, projects, tasks, time logs, and reports.

## Features

* Time logging and time tracking
* Time log and report viewing
* Project and task management
* Employee management
* Role-based access control
* Support for assigning multiple roles to a user
* Employee assignment to projects

## Roles and Permissions

The application supports three roles:

* **Admin**
* **Manager**
* **Employee**

Users can be assigned **multiple roles**.

### Admin

An admin has full access to the system and can:

* Create, read, update, and delete employees
* Create, read, update, and delete projects
* Create, read, update, and delete time logs for any employee
* Create, read, update, and delete tasks within a project
* View reports
* Assign employees to projects

### Manager

A manager can manage projects and employees within their scope.

Managers can:

* Assign employees to projects

  * Both the manager and employees must be within the manager's scope
* Update project details such as:

  * Project duration
  * Project status
* Create, read, update, and delete tasks
* View reports

### Employee

An employee has access to their own time logs.

Employees can:

* Log their own time
* View their own time logs

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* MySQL

### Frontend

* React
* Vite
* Mantine UI

### Deployment

* Docker
* Docker Compose

## Setup

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend_hand
```

Install the required npm packages:

```bash
npm i
```

## Database Setup

To create the database tables and perform the default database setup, navigate to the database setup directory:

```bash
cd backend/app/db
```

Run:

```bash
python create_tables.py
```

This will create the required database tables and perform the default setup.

## Running the Application

From the project root directory, run:

```bash
npm run dev
```

This starts the application using the development configuration.

## Running with Docker

The application can also be run using Docker Compose.

From the project root directory, run:

```bash
docker compose up
```

Docker Compose will start the required application services.
