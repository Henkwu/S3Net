from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import torch

class cub(object):
    """
    Dataset statistics:
    # 64 * 600 (train) + 16 * 600 (val) + 20 * 600 (test)
    """
    dataset_dir = '/media/space1/cvteam_wh/WH/WH/datasets/image_cub_2010/images'
    #dataset_dir = '/media/space1/cvteam_wh/WH/WH/datasets/CUB_200_2011/images_cub/images'

    def __init__(self):
        super(cub, self).__init__()
        self.train_dir = os.path.join(self.dataset_dir, 'train')
        self.val_dir = os.path.join(self.dataset_dir, 'val')
        self.test_dir = os.path.join(self.dataset_dir, 'test')
        # self.train_dir = os.path.join(self.dataset_dir, 'train.pickle')
        # self.val_dir = os.path.join(self.dataset_dir, 'val.pickle')
        # self.test_dir = os.path.join(self.dataset_dir, 'test.pickle')

        self.train, self.train_labels2inds, self.train_labelIds = self._process_dir(self.train_dir)
        self.val, self.val_labels2inds, self.val_labelIds = self._process_dir(self.val_dir)
        self.test, self.test_labels2inds, self.test_labelIds = self._process_dir(self.test_dir)

        self.num_train_cats = len(self.train_labelIds)
        num_total_cats = len(self.train_labelIds) + len(self.val_labelIds) + len(self.test_labelIds)
        num_total_imgs = len(self.train + self.val + self.test)

        print("=> cubs_dataset loaded")
        print("Dataset statistics:")
        print("  ------------------------------")
        print("  subset   | # cats | # images")
        print("  ------------------------------")
        print("  train    | {:5d} | {:8d}".format(len(self.train_labelIds), len(self.train)))
        print("  val      | {:5d} | {:8d}".format(len(self.val_labelIds),   len(self.val)))
        print("  test     | {:5d} | {:8d}".format(len(self.test_labelIds),  len(self.test)))
        print("  ------------------------------")
        print("  total    | {:5d} | {:8d}".format(num_total_cats, num_total_imgs))
        print("  ------------------------------")

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError("'{}' is not available".format(self.train_dir))
        if not osp.exists(self.val_dir):
            raise RuntimeError("'{}' is not available".format(self.val_dir))
        if not osp.exists(self.test_dir):
            raise RuntimeError("'{}' is not available".format(self.test_dir))

    def _process_dir(self, dir_path):
        cat_container = sorted(os.listdir(dir_path))
        cats2label = {cat:label for label, cat in enumerate(cat_container)}

        dataset = []
        labels = []
        for cat in cat_container:
            for img_path in sorted(os.listdir(os.path.join(dir_path, cat))):
                # if '.JPEG' not in img_path:
                if '.jpg' not in img_path:
                    continue
                label = cats2label[cat]
                dataset.append((os.path.join(dir_path, cat, img_path), label))
                labels.append(label)

        labels2inds = {}
        for idx, label in enumerate(labels):
            if label not in labels2inds:
                labels2inds[label] = []
            labels2inds[label].append(idx)

        labelIds = sorted(labels2inds.keys())
        return dataset, labels2inds, labelIds
    def _get_pair(self, data, labels):
        assert (data.shape[0] == len(labels))
        data_pair = []
        for i in range(data.shape[0]):
            data_pair.append((data[i], labels[i]))
        return data_pair
    
if __name__ == '__main__':
    cub()
    
    
    
