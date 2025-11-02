import sys
import os

import cv2
from login import Login
from logger import log
import config
from src.utility import get_project_root


def capture_and_login(output_file=None):
    log.info("main is running")
    config.load_config(os.path.join(get_project_root(), "config.json"))

    camera = cv2.VideoCapture(0)
    login_class = Login(os.path.join(get_project_root(), "db"))

    success_count = 0
    loss_count = 0
    while True:
        if loss_count >= 20:
            camera.release()
            log.error("登录失败，过多的丢帧")
            # 如果指定了输出文件，写入错误码
            if output_file:
                try:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write("000000")
                    log.info(f"Error code written to {output_file}")
                except Exception as e:
                    log.error(f"Failed to write error code: {e}")
            return "000000"

        ret, frame = camera.read()
        if not ret:
            loss_count += 1
            continue  # 跳过本次循环

        # 初始化 result
        result = 0
        try:
            result = login_class.login(frame)
        except Exception as e:
            log.error(f"Login failed: {e}")
            result = 0  # 异常时设置为失败

        if result == 0:
            loss_count += 1
        else:
            success_count += 1
            camera.release()
            password = config.get_config_value("password")

            # 转换为字符串
            password_str = str(password)
            log.info(f"Password retrieved: {password_str}")

            # 如果指定了输出文件，写入文件而不是 print
            if output_file:
                try:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(password_str)
                    log.info(f"Password written to {output_file}")
                except Exception as e:
                    log.error(f"Failed to write password: {e}")

            return password_str


if __name__ == "__main__":
    # 检查命令行参数
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    res = capture_and_login(output_file)

    # 如果没有指定输出文件，才 print（用于测试）
    if not output_file:
        print(res)
