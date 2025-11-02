# -*- coding: utf-8 -*-
# @Time : 20-6-4 下午2:13
# @Author : zhuying
# @Company : Minivision
# @File : utility.py
# @Software : PyCharm

from datetime import datetime
import os


def get_time():
    return (str(datetime.now())[:-10]).replace(" ", "-").replace(":", "-")


def get_kernel(height, width):
    kernel_size = ((height + 15) // 16, (width + 15) // 16)
    return kernel_size


def get_width_height(patch_info):
    w_input = int(patch_info.split("x")[-1])
    h_input = int(patch_info.split("x")[0].split("_")[-1])
    return w_input, h_input


def parse_model_name(model_name):
    info = model_name.split("_")[0:-1]
    h_input, w_input = info[-1].split("x")
    model_type = model_name.split(".pth")[0].split("_")[-1]

    if info[0] == "org":
        scale = None
    else:
        scale = float(info[0])
    return int(h_input), int(w_input), model_type, scale


def make_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_project_root():
    """返回项目根目录的绝对路径。
    - 打包后：exe 所在目录（与 smile2unlock_entry.exe 同级）
    - 开发时：当前工作目录（cwd）

    开发时假设用户在项目根目录运行命令（如 python generate_db.py），这是标准开发实践。
    无论从哪个目录调用，始终返回同一个根目录。
    """
    import sys

    if getattr(sys, "frozen", False):
        # 打包后：返回 exe 所在目录
        return os.path.dirname(sys.executable)
    else:
        # 开发时：使用当前工作目录作为项目根
        return os.path.abspath(os.getcwd())


def get_resource_path(*parts):
    """返回只读资源文件的绝对路径（如模型文件等打包到 _internal 的资源）。
    内部调用 get_project_root() 并拼接 'resources' 路径。

    用法:
        get_resource_path('anti_spoof_models')  -> 项目根/resources/anti_spoof_models
        get_resource_path('detection_model', 'deploy.prototxt')  -> 项目根/resources/detection_model/deploy.prototxt
    """
    import sys

    if getattr(sys, "frozen", False):
        # 打包后：优先使用 _MEIPASS（onefile 模式）
        base = getattr(sys, "_MEIPASS", None)
        if base:
            return os.path.join(base, "resources", *parts)
        # onedir 模式：使用 exe 所在目录
        return os.path.join(get_project_root(), "resources", *parts)
    else:
        # 开发时：使用项目根目录
        return os.path.join(get_project_root(), "resources", *parts)
