# Application Documentation
visit online: https://pythondemo.up.railway.app/
## Overview
This application is built using the Flask framework, a micro web framework for Python, and incorporates various technologies for efficient functionality. It follows the client-server architecture, with Flask serving as the backend (server) and HTML/CSS used for the frontend (client). The primary features include file upload handling, CSV file processing, and sorting algorithms for calculating and sorting top performers based on average grades.

## Stack
### Backend (Flask)
- **Flask:** A micro web framework for Python.
- **Jinja2:** A template engine for Python used for generating HTML pages in Flask.
- **CSV Module:** A Python module for reading and writing CSV files, used for processing uploaded grades files.
- **os Module:** A Python module providing a way to interact with the operating system, used for managing file paths and directories.

### Frontend
- **HTML:** HyperText Markup Language is used to structure content on the web page.
- **CSS (Cascading Style Sheets):** Used for styling HTML elements on the web page.

### Backend Logic
- **Python:** The programming language used for writing backend logic.
- **File Upload Handling (Flask Request Module):** The Flask request object is used for handling file uploads.
- **File System Operations:** Utilized to create directories for file uploads and manage file paths.
- **Sorting Algorithms:** Used to calculate and sort top performers based on average grades.

## Installation
1. **Clone the repository:** `git clone <repository_url>`
2. **Navigate to the project directory:** `cd <project_directory>`

## Dependencies
Install the required dependencies using pip:


pip install -r requirements.txt
## Run the Application
Execute the following command to run the Flask application:


python app.py
Visit http://localhost:5000 in your web browser to access the application.

## Alternatives to Jinja2
While Jinja2 is a popular choice, consider the following alternatives based on your preferences:

- **Mako Templates**
- **Chameleon Templates**
- **Django Templates**
- **Chevron**
- **Cheetah**

Each has its own strengths, so choose the one that best aligns with your project requirements. Feel free to explore and experiment!

