"""routes are the different URLs that the application implements"""

from app import app    # importing the app variable from the app
from flask import render_template, request, redirect  # Converts a template into a complete HTML page
import os
from werkzeug.utils import secure_filename


# File path for saving the upload
app.config["FILE_UPLOADS"] = "/Users/briagray/PycharmProjects/Project1_Prototypes/app/static/file/uploads"

# Accepted file types
app.config["ALLOWED_FILE_EXTENSIONS"] = ["GPX"]


# Checks to make sure the given file is of the correct file type
def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False


# Decorators; Modifies the function that follows it.
@app.route('/upload_file', methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if request.files:
            gpx = request.files["gpxFile"]

# Checks to make sure the file has a file name
            if gpx.filename == "":
                print("File must have a file name")
                return redirect(request.url)

# Checks to see if the file is in gpx format
            if not allowed_file(gpx.filename):
                print("That is not the correct file type")
                return redirect(request.url)

# Corrects any harmful file names
            else:
                filename = secure_filename(gpx.filename)

# If all is correct it will save the file to the given path
            gpx.save(os.path.join(app.config["FILE_UPLOADS"], filename))

            print("Image has been saved!")

# Redirects back to the initial page
            return redirect(request.url)
    return render_template("upload_file.html")
