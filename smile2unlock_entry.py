import threading
import time
from ctypes import windll

import cv2

from src import util
from src.hook import Hook
from src.logger import log
from src.login import Login


class LoginSystem:
    def __init__(self, db_dir):
        log.info("smile2unlock_entry")
        self.db_dir = db_dir

        self.camera = cv2.VideoCapture(0)
        self.success_count = 0
        self.lose_count = 0
        self.hook = Hook()
        self.login = Login(db_dir)

    def lock_screen(self):
        user32 = windll.LoadLibrary("user32.dll")
        user32.LockWorkStation()

    def process_frame(self):
        print("开始检测")
        log.info("开始检测")

        ret, frame = self.camera.read()
        if not ret:
            self.lose_count += 1
            return False

        # 去除黑边
        frame = util.remove_black_borders(frame)

        result = self.login.login(frame)
        if result == 0:
            self.lose_count += 1
        else:
            self.success_count += 1

        return True

    def start(self):
        # 启动程序控制
        threading.Thread(target=self.hook.start_program).start()
        while True:
            if self.hook.status == 0:
                log.info("hook.status==0,try to break")
                break
            if self.success_count >= 1:
                self.hook.kill_program()
                log.info("success_count>=1,try to kill hook")
                try:
                    self.hook.kill_program()
                except Exception:
                    pass
                log.info("fail")
                print("ok")
                log.info("ok")

                break

            if self.lose_count >= 120:
                try:
                    self.hook.kill_program()
                except Exception:
                    print("lose, but hook killed failed")
                    pass
                self.lock_screen()
                break

            threading.Thread(target=self.process_frame).start()
            time.sleep(0.5)


if __name__ == "__main__":
    db_dir = "./db"
    frs = LoginSystem(db_dir)
    frs.start()
