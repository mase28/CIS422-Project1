"""routes are the different URLs that the application implements"""


from flask import render_template, request  # Converts a template into a complete HTML page
import os
from werkzeug.utils import secure_filename
from flask import Flask
from map_box import *


app = Flask(__name__)    # instance of class Flask in the __init__.py script
#from app import app

# File path for saving the upload
app.config["FILE_UPLOADS"] = "./static/file/uploads"
app.config["API_KEYS_UPLOADS"] = "./static/apiKeys"

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
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if request.form.get:
            api = request.form.get("api-key")
            print(api)
            with open(os.path.join(app.config["API_KEYS_UPLOADS"], "api_key.txt"), "w") as filename:
                filename.write(api)
            print("API KEY saved.")

        if request.files:
            gpx = request.files["gpxFile"]

# Checks to make sure the file has a file name
            if gpx.filename == "":
                print("File must have a file name")
                return render_template("Wrong.html")

# Checks to see if the file is in gpx format
            if not allowed_file(gpx.filename):
                print("That is not the correct file type")
                return render_template("Wrong.html")

# Corrects any harmful file names
            else:
                filename = secure_filename(gpx.filename)

# If all is correct it will save the file to the given path
            full_path = os.path.join(app.config["FILE_UPLOADS"], filename)
            gpx.save(full_path)

            print("Image has been saved!")

            run_program(full_path, api)

# Redirects back to the initial page
            return render_template("output.html")
    return render_template("upload_file.html")


def run_program(path: str, key: str):
    """ This is where the program is called."""
    main(path, key)
    return print("Program ran")





