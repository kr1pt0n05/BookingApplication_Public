from flask import Flask, render_template, request, redirect, jsonify, session
from datetime import datetime, date
from decorators import login_required

from models import db, addUser, createAllTables, deleteAllTables, checkIn, checkOut, getEmployeeStatistics, getUserById, \
    getMonthlyTimestamps, getUserByEmail

DATABASE = "sqlite.db"
SECRET_KEY = "os.urandom(12).hex()"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
app.secret_key = SECRET_KEY
db.init_app(app)


##################################################################################################################
#  WEB ENDPOINTS. THOSE WILL USUALLY BE CALLED BY THE USER ITSELF. WILL RETURN HTML CONTENT.
##################################################################################################################

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = getUserByEmail(email)

        if user is None:
            return jsonify({"message": "User does not exist"}), 400

        if user.password != password:
            return jsonify({"message": "Invalid user credentials!"}), 401

        session["user_id"] = user.id
        return jsonify({"message": "Login successful!"}), 200


# Example to call this URL: http://127.0.0.1:5000/tms
# Returns tms page of user and insert his data, e.g. name, email, occupation.
@app.route("/tms")
@login_required
def tms():
    user_id = session["user_id"]

    if user_id:
        userData = getUserById(user_id).to_dict()
        return render_template("tms.html", user=userData)

    return "User id missing or invalid!", 400


# Example to call this URL: http://127.0.0.1:5000/statistics
# Returns statistics of a user
@app.route("/statistics")
@login_required
def statistics():
    user_id = session["user_id"]

    if user_id:
        userData = getUserById(user_id).to_dict()
        userStatistics = getEmployeeStatistics(user_id).to_dict()
        return render_template("statistics.html", user=userData, statistics=userStatistics)

    return "User id missing or invalid!", 400


# Example to call this URL: http://127.0.0.1:5000/vaq_request
# Returns formular to request vacation
@app.route("/vaq_request")
@login_required
def vaq_request():
    user_id = session["user_id"]

    if user_id:
        userData = getUserById(user_id).to_dict()
        return render_template("vaq_request.html", user=userData)

    return "User id missing or invalid!", 400

##################################################################################################################
#  API ENDPOINTS. WILL RETURN DATA IN JSON FORMAT.
##################################################################################################################

# Example to call this URL: http://127.0.0.1:5000/logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    user_id = session["user_id"]

    if user_id:
        session.pop("user_id")
        return jsonify({"message": "Logout successful!"}), 200

    return "Error logging out!", 500


# Example to call this URL: http://127.0.0.1:5000/getUserInfo
# Returns information about user, e.g. name, oemail and occupation.
# If you wish to change the format of the returned JSON, change the to_dict() of User class inside models.py!
@app.route("/getUserInfo")
@login_required
def getUserInfo():
    user_id = session["user_id"]

    if user_id:
        user = getUserById(user_id).to_dict()

        return user, 200

    return "User id missing or invalid!", 400


# Example to call this URL: http://127.0.0.1:5000/getCurrentWorktimeStatistics
# Returns flextime and vacation days in JSON format.
# If you wish to change the format of the returned JSON, change the to_dict() of EmployeeStatistics class inside models.py!
@app.route("/getCurrentWorktimeStatistics")
@login_required
def getCurrentWorktimeStatistics():
    user_id = session["user_id"]

    if user_id:
        statistics = getEmployeeStatistics(user_id).to_dict()

        return jsonify({"statistics": statistics}), 200

    return "User id missing or invalid!", 400


# Example to call this URL: http://127.0.0.1:5000/getMonthlyTimestamps
@app.route("/getMonthlyTimestamps", methods=["POST"])
@login_required
def getMonthlyTimestamps_():
    user_id = session["user_id"]

    if user_id:
        data = request.get_json()
        year = data.get("year")
        month = data.get("month")
        timestamps = getMonthlyTimestamps(user_id, month, year)
        timestamps_json = []

        for ts in timestamps:
            timestamps_json.append(ts.to_dict())

        return jsonify({"timestamps": timestamps_json}), 200

    return jsonify({"message": "User id missing or invalid!"}), 400


# Example to call this URL: http://127.0.0.1:5000/check-in
# Change user_id to check in corresponding user.
# Returns bad status code, if user_id is not provided, invalid or already checked in.
@app.route("/check-in")
@login_required
def checkIn_():
    user_id = session["user_id"]

    if user_id:
        date_ = date.today()
        time_ = datetime.now().time().strftime("%H:%M")
        time__ = datetime.strptime(time_, "%H:%M").time()

        if checkIn(user_id, date_, time__):
            return "Checked In!", 200

    return "User id missing or invalid!", 400


# Example call to this URL: http://127.0.0.1:5000/check-out
# Change user_id to check in corresponding user.
# Returns bad status code, if user_id is not provided, invalid or already checked out.
@app.route("/check-out")
@login_required
def checkOut_():
    user_id = session["user_id"]

    if user_id:
        date_ = date.today()
        time_ = datetime.now().time().strftime("%H:%M")
        time__ = datetime.strptime(time_, "%H:%M").time()

        if checkOut(user_id, date_, time__):
            return "Checked Out!", 200

    return "User id missing or invalid!", 400


##################################################################################################################
#  URLS FOR DEBUGGING PURPOSES. WILL NOT BE USED IN PRODUCTION DEPLOYMENT.
##################################################################################################################

# Generates Test Data
# Example call to this URL: http://127.0.0.1:5000/testdata
@app.route("/testdata")
def testData():
    # createAllTables()
    # deleteAllTables()
    # addUser("Anderson", "Rolf", "randommail@yahoo.de", "meinPW")

    testuser = [
        ("Anderson", "Rolf", "randommail@yahoo.de", "meinPW", "Facility Management"),
        ("Wiener", "Hans-Jürgen", "hj-wiener@gmail.com", "123456"),
        ("Siemens", "Bertha", "ichhabeuchallelieb@outlook.com", "ganzSicheresPasswort", "Senior Developer")
    ]

    timestamps_in = [
        (1, datetime.strptime("2024-11-01", "%Y-%m-%d"), datetime.strptime("07:55:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-02", "%Y-%m-%d"), datetime.strptime("08:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-10", "%Y-%m-%d"), datetime.strptime("07:50:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-15", "%Y-%m-%d"), datetime.strptime("09:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-20", "%Y-%m-%d"), datetime.strptime("06:45:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-01", "%Y-%m-%d"), datetime.strptime("07:45:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-05", "%Y-%m-%d"), datetime.strptime("09:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-10", "%Y-%m-%d"), datetime.strptime("08:15:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-12", "%Y-%m-%d"), datetime.strptime("10:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-15", "%Y-%m-%d"), datetime.strptime("08:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-01", "%Y-%m-%d"), datetime.strptime("08:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-03", "%Y-%m-%d"), datetime.strptime("09:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-06", "%Y-%m-%d"), datetime.strptime("07:55:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-10", "%Y-%m-%d"), datetime.strptime("08:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-15", "%Y-%m-%d"), datetime.strptime("09:45:00", "%H:%M:%S").time())
    ]

    timestamps_out = [
        (1, datetime.strptime("2024-11-01", "%Y-%m-%d"), datetime.strptime("13:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-02", "%Y-%m-%d"), datetime.strptime("17:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-10", "%Y-%m-%d"), datetime.strptime("13:15:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-15", "%Y-%m-%d"), datetime.strptime("18:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-11-20", "%Y-%m-%d"), datetime.strptime("15:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-01", "%Y-%m-%d"), datetime.strptime("15:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-05", "%Y-%m-%d"), datetime.strptime("17:15:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-10", "%Y-%m-%d"), datetime.strptime("16:45:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-12", "%Y-%m-%d"), datetime.strptime("18:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2024-12-15", "%Y-%m-%d"), datetime.strptime("14:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-01", "%Y-%m-%d"), datetime.strptime("16:00:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-03", "%Y-%m-%d"), datetime.strptime("17:45:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-06", "%Y-%m-%d"), datetime.strptime("18:30:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-10", "%Y-%m-%d"), datetime.strptime("17:15:00", "%H:%M:%S").time()),
        (1, datetime.strptime("2025-01-15", "%Y-%m-%d"), datetime.strptime("14:30:00", "%H:%M:%S").time())
    ]

    for user in testuser:
        addUser(*user)

    for i in range(13):
        checkIn(*timestamps_in[i])
        checkOut(*timestamps_out[i])

    return "Generated Test Data!", 200


# Example call to this URL: http://127.0.0.1:5000/deleteAllTables
@app.route("/deleteAllTables")
def deleteAllTables_():
    deleteAllTables()
    return "Deleted all Tables!", 200


# Example call to this URL: http://127.0.0.1:5000/createAllTables
@app.route("/createAllTables")
def createAllTables_():
    createAllTables()
    return "Created all Tables!", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
