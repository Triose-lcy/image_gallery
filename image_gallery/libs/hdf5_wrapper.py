import h5py
from libs.image_wrapper import ImageWrapper


class Hdf5Wrapper:

    def __init__(self, _h5_path=None):
        self.h5_path = _h5_path
        self.h5_handler = None

    def init_handler(self, mode='r'):
        self.h5_handler = h5py.File(self.h5_path, mode)

    def free_handler(self):
        self.h5_handler.close()

    def create_group(self, group_name):
        try:
            self.h5_handler.create_group(group_name)
        except:
            return False
        return True

    def write_image_wrapper_into_group(self, group_name, img_wrapper):
        return self.write_singe_into_group(group_name, img_wrapper.get_filename(), img_wrapper.get_ndarr())

    def read_image_wrapper_from_group(self, group_name, dataset_name):
        ret = ImageWrapper()
        tmp_ndarr = self.read_single_from_group(group_name, dataset_name)
        if not tmp_ndarr:
            return None
        ret.set_ndarr(tmp_ndarr)
        ret.set_filename(dataset_name)
        return ret

    def write_singe_into_group(self, group_name, dataset_name, dataset_value):
        """
        Create a dataset in a group
        :param dataset_name:
        :param dataset_value:
        :return:
        """
        try:
            self.h5_handler[group_name].create_dataset(name=dataset_name, data=dataset_value)
        except:
            return False
        return True

    def read_single_from_group(self, group_name, dataset_name):
        """
        Read data from a group
        :param group_name:
        :param dataset_name:
        :return: a np ndarray or None
        """
        ret = None
        try:
            ret = self.h5_handler[group_name][dataset_name].value
        except:
            return ret
        return ret
