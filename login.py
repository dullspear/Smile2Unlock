import datetime
import os
from src.fake_face_test import test
from src import util
from src.utility import get_resource_path
from logger import log


class Login:
    def __init__(self, db_dir):
        self.db_dir = db_dir

    def login(self, img_arr):
        print("开始登录")
        log.info("开始登录")
        label = test(
            image=img_arr,
            model_dir=get_resource_path("anti_spoof_models"),
            device_id=0,
        )
        if label == 1:
            name = util.recognize(img_arr, self.db_dir)
            # log db_dir 相对路径
            log.info(f"相对路径：db_dir: {self.db_dir}")
            # log db_dir 绝对路径
            log.info(f"绝对路径：db_dir: {os.path.abspath(self.db_dir)}")

            if name in "unknown_person":
                print("unknown_person")
                log.info("unknown_person")
                return 0
            elif name in "no_persons_found":
                print("no_persons_found")
                log.info("no_persons_found")
                return 0
            else:
                log.info(f"{name},{datetime.datetime.now()},in")
                log.info("成功")
                return 1
        else:
            print("假脸")
            log.info("假脸")
            return 0
