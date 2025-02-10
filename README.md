# Django To-Do Manager

## Project Overview

This is a simple To-Do Manager web application built with Django, designed to help users manage their projects and tasks efficiently. The application provides a user-friendly interface for creating, updating, and tracking tasks.

## Features

- Create and manage projects
- Add, edit, and delete tasks
- Task prioritization
- Responsive web design
- HTMX integration for dynamic interactions

## Prerequisites

- Python 3.12
- Poetry (Dependency Management)
- Docker (Optional, for containerized deployment)

## Technology Stack

- Backend: Django 5.1.5
- Python Version: 3.12
- Database: SQLite (default) / MySQL (configurable)
- Frontend: HTML, JavaScript, HTMX
- Deployment: Docker support

## Configuration

Create a `.env` file in the project root with the following configuration:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your_very_long_and_random_secret_key_here

# MySQL Database Configuration
MYSQL_DATABASE=todo_manager_db
MYSQL_ROOT_USER=root
MYSQL_ROOT_PASSWORD=strong_root_password

MYSQL_USER=todo_app_user
MYSQL_PASSWORD=secure_user_password
PORT=8000
```

Notes:

- Replace placeholder values with your actual secure credentials
- Never commit `.env` to version control
- Use a strong, unique SECRET_KEY

## Installation

### Local Development Setup

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   cd to-do-manager
   ```

2. Install Poetry (if not already installed):

   ```bash
   pip install poetry
   ```

3. Install project dependencies:

   ```bash
   poetry install
   ```

4. Activate the virtual environment:

   ```bash
   poetry shell
   ```

5. Run database migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

### Docker Deployment

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

## Running Tests

### Local Test Runner

```bash
poetry run pytest
```

### Docker Test Runner

```bash
docker-compose -f docker-compose-test.yaml run --rm test pytest
```

## Project Structure

- `config/`: Django project configuration
- `tasks/`: Main application module
  - `models.py`: Database models
  - `views.py`: View logic
  - `templates/`: HTML templates
  - `static/`: CSS, JavaScript, and images
  - `tests/`: Test cases for models and views

## How to Use the App

### Getting Started

1. **Authentication**

   - Sign up or log in to access the application
   - _Note_: After login/signup, refresh the page to ensure proper functionality

2. **Creating Projects**

   - Click on the calendar icon to create a new project
   - Specify the project date
   - Tasks that were created on this date will be automatically grouped into the project

3. **Managing Tasks**

   - Click the "Add task" button to add a new task
   - Date selector is available near the add task button
   - Tasks can be:
     - Edited
     - Deleted
     - Reprioritized
     - Grouped into a project (if there is no project for a date, but there are task they can be grouped into a project)

4. **Task Organization**
   - Tasks are automatically grouped by their creation date
   - Projects help categorize and manage related tasks
   - Use date selection to create context-specific task lists

### Notes

**Authentication and Page Reloading**

- After login, signup, or signout, refresh the page manually
- Use browser refresh (F5) to ensure all features load correctly
- This helps resolve potential routing or loading issues

**Potential improvements for future versions**:

- Implement more robust HTMX-based page transitions
- Enhance client-side routing mechanisms
- Add explicit redirect handling in authentication views

## Tips

- Always check the date when creating tasks
- Utilize project grouping for better task management
- Regularly update and reprioritize your tasks
