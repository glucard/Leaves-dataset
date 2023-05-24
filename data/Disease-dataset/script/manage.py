from PIL import Image
import os, shutil

def create_paths(paths):
    for p in paths:
        if not os.path.exists(p):
            os.mkdir(p)

def train_val_paths(path):

    p_train = path + os.sep + 'train'
    p_val = path + os.sep + 'val'

    create_paths([path, p_train, p_val])

    return p_train, p_val

def paths_join(paths, join_path):

    paths_new = []

    for p in paths:
        p_new = p + os.sep + join_path
        paths_new.append(p_new)
    
    create_paths(paths_new)

    return paths_new

class Manager:
    def __init__(self):
        pass

    def split(path_in, path_out, train_count):
        """
        Split the raw dataset into 2 datasets using a const
        and save into a new folder
        """
        p_in = path_in
        p_out = path_out
        t_c = train_count

        p_train, p_val = train_val_paths(p_out)

        classes_in = os.listdir(p_in)
        for class_in in classes_in:
            p_class_in, p_class_train, p_class_val = paths_join([p_in, p_train, p_val], class_in)

            imgs_in = os.listdir(p_class_in)
            for i, img_in in enumerate(imgs_in):
                
                p_img_in = p_class_in + os.sep + img_in

                if i < t_c:
                    p_img_out = p_class_train + os.sep + img_in
                else:
                    p_img_out = p_class_val + os.sep + img_in

                shutil.copy(p_img_in, p_img_out)

    def only_classes(p_in, p_out):
        datasets = os.listdir(p_in)
        create_paths([p_out])
        for dataset in datasets:
            p_dataset_in = os.path.join(p_in, dataset)
            p_dataset_out = os.path.join(p_out, dataset)
            create_paths([p_dataset_out])
            classes_in = os.listdir(p_dataset_in)
            for class_in in classes_in:
                class_out = class_in.split("_")[0]
                
                p_class_in = os.path.join(p_dataset_in, class_in)
                p_class_out = os.path.join(p_dataset_out, class_out)
                create_paths([p_class_out])
                imgs_in = os.listdir(p_class_in)
                for img_in in imgs_in:
                    p_img_in = os.path.join(p_class_in, img_in)
                    p_img_out = os.path.join(p_class_out, img_in)
                    shutil.copy(p_img_in, p_img_out)

    def diases_dataset(path_in, path_out):
        """
        creates a dataset containing each leaf disease
        """
        p_in = path_in
        p_out = path_out

        create_paths([p_out])

        classes_in = os.listdir(p_in)
        for class_in in classes_in:

            class_name_splitted = class_in.split('__')
            class_out = class_name_splitted[1][1:] if len(class_name_splitted) == 2 else 'Background'

            p_class_in = os.path.join(p_in, class_in)
            p_class_out = os.path.join(p_out, class_out)

            create_paths([p_class_out])
            imgs_in = os.listdir(p_class_in)
            for img_in in imgs_in:
                
                p_img_in = p_class_in + os.sep + img_in
                p_img_out = p_class_out + os.sep + img_in

                shutil.copy(p_img_in, p_img_out)

    def diases_datasets_by_leaf(path_in, path_out):
            """
            creates a dataset containing each leaf disease
            """
            p_in = path_in
            p_out = path_out

            create_paths([p_out])

            classes_in = os.listdir(p_in)
            for class_in in classes_in:

                class_name_splitted = class_in.split('__')

                leaf_name = class_name_splitted[0]
                class_out = class_name_splitted[1][1:] if len(class_name_splitted) == 2 else 'Background'

                p_class_in = os.path.join(p_in, class_in)

                p_class_out, = paths_join([p_out], leaf_name)

                p_class_out, = paths_join([p_class_out], class_out)

                imgs_in = os.listdir(p_class_in)
                for img_in in imgs_in:
                    
                    p_img_in = p_class_in + os.sep + img_in
                    p_img_out = p_class_out + os.sep + img_in

                    shutil.copy(p_img_in, p_img_out)

if __name__ == "__main__":
    path_in = '.tempdataset/1_raw'
    path_out = '.tempdataset/diases_datasets_by_leaf'
    Manager.diases_datasets_by_leaf(path_in, path_out)
    """
    path_out_2 = '2_separeted'
    path_out_3 = '3_leaf_classes'
    Manager.split(path_in, path_out_2, 7)
    Manager.only_classes(path_out_2, path_out_3)
    """