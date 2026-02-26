# @Time : 20-6-4 下午2:13
# @Author : zhuying
# @Company : Minivision
# @File : utility.py
# @Software : PyCharm

import os
from datetime import datetime


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


def get_base_path():
    """返回运行时资源基准路径：
    - 如果程序被 PyInstaller 打包（frozen），优先使用 sys._MEIPASS（onefile）
      否则使用 exe 所在目录；
    - 开发模式下返回源码目录。
    """
    import sys

    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", None)
        if base:
            return base
        return os.path.dirname(sys.executable)

    # 非打包时使用当前工作目录作为项目根（用户要求：运行 py 时 cwd 即为项目根）
    return os.path.abspath(os.getcwd())


def resource_path(*parts):
    """返回资源的运行时绝对路径（相对于 project base）。
    用法: resource_path('resources', 'detection_model', 'deploy.prototxt')
    """
    base = get_base_path()
    return os.path.join(base, *parts)


def output_dir():
    """返回用于写入/生成文件的目录（可写）。对于 exe，使用 exe 同目录；开发模式使用源码目录。"""
    import sys

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    # 开发模式下使用当前工作目录
    return os.path.abspath(os.getcwd())
