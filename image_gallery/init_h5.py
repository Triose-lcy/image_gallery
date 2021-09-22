from libs.hdf5_wrapper import Hdf5Wrapper

if __name__ == '__main__':
    h5wrapper = Hdf5Wrapper(_h5_path="./hdf5/image_repo.h5")
    h5wrapper.init_handler(mode="w")

    res = h5wrapper.create_group(group_name="raw_images")
    print(res)

    h5wrapper.free_handler()
