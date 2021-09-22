import cv2
import base64
import numpy as np
from werkzeug.utils import secure_filename




def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ImageWrapper:

    def __init__(self):
        self.ndarr = None
        self.filename = None

    def get_ndarr(self):
        return self.ndarr

    def set_ndarr(self, _ndarr):
        self.ndarr = _ndarr

    def get_filename(self):
        return self.filename

    def set_filename(self, _filename):
        self.filename = _filename

    def build_from_filestorage(self, file_storage=None):
        """
        Build an ImageWrapper object from a file_storage object
        :param file_storage: werkzeug.datastructures.FileStorage object
        :return: True/False (if succeed, return true)
        """
        if not file_storage:
            return False
        if not allowed_file(file_storage.filename):
            return False
        try:
            self.ndarr = cv2.imdecode(np.frombuffer(file_storage.read(), np.uint8), cv2.IMREAD_COLOR).astype(np.float32)
            self.filename = secure_filename(file_storage.filename)
        except:
            # If there is any exception, return false
            # TODO: specify exceptions
            return False
        return True

    def to_b64(self, rgb2bgr=False):
        """
        Converts self.ndarr to a b64 string readable by html-img tags
        :return:
        """
        ret = None
        try:
            img = self.ndarr
            if rgb2bgr:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.png', img)
            ret = base64.b64encode(buffer).decode('utf-8')
        except:
            # If anything happens, return None
            # TODO: specify exceptions
            return ret
        return ret

    def img_resize(self, new_size=(300, 300)):
        """
        Resizes self.ndarr to given size
        :param size: 2d
        :return: A numpy ndarray
        """
        ret = None
        try:
            ret = cv2.resize(self.ndarr, new_size)
        except:
            return ret
        return ret

    @staticmethod
    def static_img_resize(ndarr, new_size=(300, 300)):
        ret = None
        try:
            ret = cv2.resize(ndarr, new_size)
        except:
            return ret
        return ret


