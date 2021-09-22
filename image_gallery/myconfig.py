import os

conf_dev, conf_prod = dict(), dict()


# Configuration of development
conf_dev["flask_conf"] = {
    "static_url_path": "",
    "static_folder": "templates/",
    "template_folder": "templates/templates/admin"
}
conf_dev["app_secret_key"] = "dev secret key"
conf_dev["app_conf"] = {
    "TMP_FOLDER_ABS": "templates/tmp/",
    "TMP_FOLDER_REL": "tmp/",
    "IMAGES_FOLDER_ABS": "templates/image_repo/",
    "IMAGES_FOLDER_REL": "image_repo/"
}
conf_dev["image_repo_path"] = "./hdf5/image_repo.h5"

# Configuration of deployment


conf = conf_dev if not os.environ.get("DEPLOYMENT", None) else conf_prod
