from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from random import randint
from myconfig import conf
import cv2
import numpy as np
from libs.object_detection import inference_by_ssd


# app = Flask(__name__,
#             static_url_path="",
#             static_folder="templates/",
#             template_folder="templates/templates/admin")
# app.config['TMP_FOLDER_ABS'] = "templates/tmp/"
# app.config['TMP_FOLDER_REL'] = "tmp/"
# app.config['IMAGES_FOLDER_ABS'] = "templates/image_repo/"
# app.config['IMAGES_FOLDER_REL'] = "image_repo/"


# load flask app configuration (from myconfig.py)
app = Flask(__name__, **conf["flask_conf"])
app.secret_key = conf["app_secret_key"]
app.config.update(conf["app_conf"])


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index_():
    return render_template("index.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/image_search", methods=['POST', 'GET'])
def image_search():
    if request.method == "POST" and request.form["search_term"].strip():
        search_term = request.form["search_term"]
        return render_template("image_search.html", search_term=search_term)

    if 'file' not in request.files:
        # first time open the image_search.html page
        return render_template("image_search.html")
    else:
        file = request.files['file']
        if file and allowed_file(file.filename):

            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            img = img.astype(np.float32)

            filename = secure_filename(file.filename)
            new_filename = str(randint(0, 4)) + "." + filename.split(".")[-1]      # TODO
            abs_image_path = os.path.join(app.config['TMP_FOLDER_ABS'], new_filename)
            rel_image_path = os.path.join(app.config['TMP_FOLDER_REL'], new_filename)
            cv2.imwrite(abs_image_path, img)

            img_resized = cv2.resize(img, (300, 300))
            img_objs = inference_by_ssd.inference(img_resized, "0.0.0.0:8500")
            print(img_objs.shape)
            print(img_objs)

            return render_template('image_search.html', filepath=rel_image_path)
        elif not file.filename:
            flash('No file selected')
            return redirect(request.url)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)


@app.route("/image_upload", methods=['POST', 'GET'])
def image_upload():
    if request.method == "POST":

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        valid_file_cnt = 0
        for file in files:
            if file and allowed_file(file.filename):
                valid_file_cnt += 1
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['IMAGES_FOLDER_ABS'], filename))

        flash("Uploaded " + str(valid_file_cnt) + " image(s)")
        return redirect(request.url)

    else:
        return render_template("image_upload.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
