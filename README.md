# SWT Waterfall: Time Tracking System

## Table of Contents

1. [About the Project](#über-das-projekt)  
2. [Technologies Used](#verwendete-technologien)  
3. [Installation](#installation)  

---

## About the Project
A simple time-tracking app that allows employees to log in, clock in and 
out, and request vacation time. Work hours are displayed in a calendar for
easy tracking and management.

---

## Used Technologies


* [![Flask][Flask]][Flask-url]
* [![SQLite][SQLite]][SQLite-url]

---

## Installation

### Requirements

- Python 3.10 installed.
- `pip` for managing python packages.

### Steps

1. **Clone Repository**:  
```bash
git clone https://github.com/kr1pt0n05/SWT-Scrum-Project.git
```
   
2. **Activate Python Virtual Environment**:  
2.1 *Windows*
   ```bash
   .venv/Scripts/activate.bat
   ```
   
   2.2 *Linux*
      ```bash
      source .venv/bin/activate
      ```

3. **Install required python packages**:
```bash
python -m pip install -r requirements.txt
```


4. **Run application**:
```bash
python3 app.py
```


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/

[SQLite]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/
