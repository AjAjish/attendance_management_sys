# Attendance Management System

An attendance management system designed for Sir Ramanujar Engineering College CSE Department to streamline and automate the process of tracking student attendance.

## 📋 Overview

This web-based application provides an efficient solution for managing student attendance records in the Computer Science and Engineering (CSE) Department. The system allows faculty members to mark, track, and generate reports on student attendance with ease.

## 🚀 Features

- **User Authentication**: Secure login system for administrators, faculty, and students
- **Attendance Marking**: Quick and easy attendance marking interface for faculty
- **Real-time Tracking**: Monitor attendance records in real-time


## 🛠️ Technology Stack

- **Backend**: Python
- **Frontend**: HTML, CSS, JS
- **Web Framework**: Django
- **Database**: MySQL

## 📁 Project Structure
```
attendance_management_sys/                     # Root folder of your project
│
├── manage.py                                  # Django's management script for running commands
├── data.py                                    # Script for loading JSON data into the models
├── requirements.txt                           # Lists all dependencies for the project
│
├── attendance_management_sys/                 # Project settings folder
│   ├── __init__.py                            # Marks this directory as a Python package
│   ├── asgi.py                                # ASGI config for deployment
│   ├── settings.py                            # Django settings file
│   ├── urls.py                                # URL routing for the entire project
│   └── wsgi.py                                # WSGI config for deployment
│
└── myapp/                                     # Your main app folder (you can have multiple apps in a Django project)
    ├── __init__.py                            # Marks this directory as a Python package
    ├── admin.py                               # Register models for the Django admin site
    ├── apps.py                                # App configuration
    ├── migrations/                            # Database migrations folder
    │   └── __init__.py                        # Marks migrations directory as a Python package
    ├── models.py                              # Define your models (database schema) here
    ├── tests.py                               # Test cases for your app
    ├── urls.py                                # URL routing specific to this app
    ├── views.py                               # Views to render the responses (logic for page rendering)
    │
    ├── templates/                             # Template folder for HTML files
    │   ├── base/                              # Shared base template for layout
    │   │   └── base.html                      # Base HTML file for layout
    │   ├── home.html                          # Home page template
    │
    └── static/                                # Static files like CSS, JS, images
        └── myapp/
            ├── css/
                └── style.css
            
```
## 🔧 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AjAjish/attendance_management_sys.git
   cd attendance_management_sys
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure MySQL database** in `attendance_management_sys/settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```


6. **Configure the database**
   ```bash
   # Update database configuration in config file
   # Run database migrations (if applicable)
   python manage.py migrate
   ```

7.**Run the application**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   
   Open your web browser and navigate to `http://localhost:5000`


## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is developed for Sir Ramanujar Engineering College CSE Department.

## 👥 Authors

- **AjAjish** - [GitHub Profile](https://github.com/AjAjish)

## 📧 Contact

For any queries or support, please contact the CSE Department at Sir Ramanujar Engineering College.

## 🙏 Acknowledgments

- Sir Ramanujar Engineering College
- CSE Department Faculty
- All contributors to this project


---

**Note**: This system is specifically designed for Sir Ramanujar Engineering College CSE Department. Please ensure you have the necessary permissions before deployment.
