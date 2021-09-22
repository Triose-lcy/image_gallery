from myconfig import conf
from datetime import datetime
from libs.image_wrapper import ImageWrapper
from libs.hdf5_wrapper import Hdf5Wrapper
from flask import Flask, flash, request, redirect, render_template


# load flask app configuration (from myconfig.py)
app = Flask(__name__, **conf["flask_conf"])
app.secret_key = conf["app_secret_key"]
app.config.update(conf["app_conf"])


@app.route("/")
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
        img_wrapper = ImageWrapper()
        img_wrapper_valid = img_wrapper.build_from_filestorage(request.files['file'])
        if not img_wrapper_valid:
            flash("Read image error")
            return redirect(request.url)
        else:
            uploaded_filestream = img_wrapper.to_b64()
            if not uploaded_filestream:
                flash("Image load error")
            return render_template("image_search.html", uploaded_filestream=uploaded_filestream)


@app.route("/image_upload", methods=['POST', 'GET'])
def image_upload():
    if request.method == "POST":

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        valid_file_cnt = 0

        h5_writer = Hdf5Wrapper(_h5_path=conf["image_repo_path"])
        h5_writer.init_handler(mode='a')

        for file in files:
            # %Y%m%d%H%M%S
            img_wrapper = ImageWrapper()
            if img_wrapper.build_from_filestorage(file):
                # Avoid duplicated name of different images
                # TODO: remove same images with same or different name(s)
                img_wrapper.set_filename(_filename=img_wrapper.get_filename() + "_" + datetime.now().strftime('%Y%m%d%H%M%S'))
                res = h5_writer.write_image_wrapper_into_group(group_name="raw_images", img_wrapper=img_wrapper)
                valid_file_cnt += res if res is not None else 0

        h5_writer.free_handler()

        flash("Uploaded " + str(valid_file_cnt) + " image(s)")
        return redirect(request.url)

    else:
        return render_template("image_upload.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
