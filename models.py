from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract, asc

db = SQLAlchemy()


#############################################################################
# User Model
# Mainly handling login
#############################################################################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    job_description = db.Column(db.String)
    role = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "surname": self.surname,
            "name": self.name,
            "email": self.email,
            "job_description": self.job_description
        }


# Return first user which matches given email
# Will return None if no match found.
def getUserByEmail(email):
    return User.query.filter_by(email=email).first()


# Adds a new user to the database.
#   Mandatory: surname, name, email, password.
#   optional: role, default: "Employee"; job_description, default: "Software Developer".
# Will also insert a new EmployeeStatistics entry.
# Important: Make sure all tables have been created before calling this function!
def addUser(surname, name, email, password, job_description="Software Developer", role="Employee"):
    new_user = User(surname=surname, name=name, email=email, password=password, job_description=job_description,
                    role=role)
    db.session.add(new_user)
    db.session.commit()

    new_statistics = EmployeeStatistics(vacation_days=10, flex_time=120, user_id=new_user.id)
    db.session.add(new_statistics)
    db.session.commit()


def getUserById(user_id):
    user = User.query.get(user_id)
    return user


# Will return statistics of an employee.
# Will return error, if none or multiple EmployeeStatistics are found for the given id.
def getEmployeeStatistics(user_id):
    statistics = EmployeeStatistics.query.filter_by(user_id=user_id).one()
    return statistics


# Will set the vacation days of an employee to the given days.
# Warning: Will NOT VALIDATE if employee got enough vacation days left!
def setRemainingVacationDays(user_id, days):
    EmployeeStatistics.query.filter_by(user_id=user_id).update({
        EmployeeStatistics.vacation_days: days
    })
    db.session.commit()


# Will set the flex time of an employee to the given time (minutes).
def setFlexTime(user_id, time_min):
    EmployeeStatistics.query.filter_by(user_id=user_id).update({
        EmployeeStatistics.flex_time: time_min
    })


#############################################################################
# Employee Statistics
# Keeping track of working statistics of Employee
#############################################################################
class EmployeeStatistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vacation_days = db.Column(db.Integer)
    flex_time = db.Column(db.Float)

    # Used to find the latest timestamp, when checking out.
    latest_timestamp_id = db.Column(db.Integer)

    # Indicating if employee is currently clocked in or out.
    # True if clocked in, False if clocked out.
    clocked_in = db.Column(db.Boolean, default=False)

    # Unidirectional relationship to EmployeeStatistics
    user_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "vacation_days": self.vacation_days,
            "flex_time": self.flex_time,
            "clocked_in": self.clocked_in
        }


#############################################################################
# Abstract TimeRecord
# Tracking time, date, approval and submission.
#############################################################################
class TimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    startTime = db.Column(db.Time)
    endTime = db.Column(db.Time)
    approved = db.Column(db.Boolean, default=False)
    approvedBy = db.Column(db.String)
    submitted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "startDate": {
                "year": self.startDate.year,
                "month": self.startDate.month,
                "day": self.startDate.day
            },
            "endDate": {
                # Check if endDate exists before trying to access its properties
                "year": self.endDate.year if self.endDate else None,
                "month": self.endDate.month if self.endDate else None,
                "day": self.endDate.day if self.endDate else None
            },
            "startTime": {
                "hour": self.startTime.hour,
                "minute": self.startTime.minute
            },
            "endTime": {
                # Check if endTime exists before trying to access its properties
                "hour": self.endTime.hour if self.endTime else None,
                "minute": self.endTime.minute if self.endTime else None
            },
            "approved": self.approved,
            "approvedBy": self.approvedBy,
            "submitted": self.submitted
        }


#############################################################################
# Time Stamp
# Inherits from TimeRecord.
#############################################################################
class TimeStamp(TimeRecord):
    workTimeMinutes = db.Column(db.Float, default=0)


# Returns all timestamps of a user of a month.
# Will order the timestamps by startDate and startTime in ascending order.
# Will order by day in ascending order.
def getMonthlyTimestamps(user_id, month, year):
    query = TimeStamp.query.filter_by(
        user_id=user_id) \
        .filter(extract("year", TimeStamp.startDate) == year) \
        .filter(extract("month", TimeStamp.startDate) == month) \
        .order_by(asc(TimeRecord.startDate), asc(TimeRecord.startTime))

    timestamps = query.all()
    return timestamps


# Starts time tracking of an employee.
# Will only start tracking of time, if user is not already clocked in.
# Will set clocked_in of EmployeeStatistics to true.
# Will set latest_timestamp of EmployeeStatistics to current timestamp's id.
# Will return true if successful, otherwise false.
def checkIn(user_id, startDate, startTime):
    statistics = getEmployeeStatistics(user_id)

    if not statistics.clocked_in:
        new_ts = TimeStamp(user_id=user_id, startDate=startDate, startTime=startTime)
        db.session.add(new_ts)
        db.session.commit()

        statistics.clocked_in = True
        statistics.latest_timestamp_id = new_ts.id
        db.session.commit()

        return True

    return False


# Stops time tracking of employee.
# Will only stop tracking of time, if user is already clocked in.
# Will set clocked_in of EmployeeStatistics to false.
# Will return true if successful, otherwise false.
# Will calculate workTime using calculateWorktimeMinutes() and add it to current flextime and the corresponding TimeStamps workTimeMinutes.
# Warning: Will not check, whether startDate and endDate equal each other.
def checkOut(user_id, endDate, endTime):
    statistics = getEmployeeStatistics(user_id)

    if statistics.clocked_in:
        ts = TimeStamp.query.get(statistics.latest_timestamp_id)
        ts.endDate = endDate
        ts.endTime = endTime

        minutes = calculateWorktimeMinutes(ts.startTime, endTime)
        ts.workTimeMinutes += minutes
        statistics.flex_time += minutes

        db.session.commit()

        statistics.clocked_in = False
        db.session.commit()

        return True

    return False


# Takes two Time objects and calculates the difference in minutes.
def calculateWorktimeMinutes(startTime, endTime):
    st_hours = startTime.hour
    st_minutes = startTime.minute
    et_hours = endTime.hour
    et_minutes = endTime.minute

    minutes = (et_hours * 60 + et_minutes) - (st_hours * 60 + st_minutes)
    print(minutes)
    return minutes


#############################################################################
# Helper functions
#############################################################################

# Create all tables, specified in this file.
# Each table corresponds to a class.
# Needs to be called before data can be inserted into the tables.
def createAllTables():
    db.create_all()


# Delete all existing tables.
def deleteAllTables():
    db.drop_all()
