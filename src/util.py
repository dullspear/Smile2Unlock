import os
import pickle

import tkinter as tk
from tkinter import messagebox

from logger import log

import cv2


def remove_black_borders(frame):
    """
    移除图像四周的黑边（Letterbox/Pillarbox）。
    原理：检测非零像素（亮度>1）的最小外接矩形，并在此范围内裁剪。
    这通常能解决摄像头驱动强制填充黑边的问题。
    """
    if frame is None:
        return frame

    # 转灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 简单的二值化，阈值设为1 (过滤掉纯黑0)
    # 如果摄像头黑边有噪点，可以适当提高阈值为 5 或 10
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # 查找非零像素点
    points = cv2.findNonZero(thresh)

    if points is not None:
        x, y, w, h = cv2.boundingRect(points)

        # 只有在确实需要裁剪时才操作
        h_src, w_src = frame.shape[:2]
        if w < w_src or h < h_src:
            return frame[y : y + h, x : x + w]

    return frame


def try_disable_dlib_cuda() -> None:
    """Best-effort disable CUDA in dlib.

    目标：在 AMD / 无 NVIDIA / 驱动不匹配的机器上，避免 dlib 在导入/首次使用时
    触发 CUDA 初始化导致的崩溃。

    注意：如果安装了正确的 CPU 版本 dlib，通常不需要此函数。
    """

    try:
        import dlib  # type: ignore

        if hasattr(dlib, "DLIB_USE_CUDA"):
            try:
                dlib.DLIB_USE_CUDA = False
            except Exception:
                pass

        if hasattr(dlib, "set_dnn_prefer_smallest_algorithms"):
            try:
                dlib.set_dnn_prefer_smallest_algorithms()
            except Exception:
                pass
    except Exception:
        return


def safe_import_face_recognition():
    """Safe import face_recognition with CUDA RuntimeError fallback.

    如果首次 import 因 CUDA 初始化失败，会自动启用 CPU 兜底并重新 import 一次。
    返回：face_recognition 模块
    """
    import sys

    try:
        import face_recognition

        return face_recognition
    except RuntimeError as e:
        msg = str(e)
        is_cuda_err = ("cudaGetDevice" in msg) or ("CUDA" in msg)
        if not is_cuda_err:
            raise

        log.warning(
            "import face_recognition RuntimeError (likely CUDA init). Enabling CPU guard then re-import. err=%s",
            msg,
        )
        try_disable_dlib_cuda()

        # 清除已加载的模块，强制重新导入
        for mod in ["face_recognition", "dlib"]:
            if mod in sys.modules:
                del sys.modules[mod]

        import face_recognition

        log.info("face_recognition re-imported successfully after CPU guard")
        return face_recognition


def get_button(window, text, color, command, fg="white"):
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=("Helvetica bold", 20),
    )

    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    face_recognition = safe_import_face_recognition()

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return "no_persons_found"
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, "rb")
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces(
            [embeddings], embeddings_unknown, tolerance=0.5
        )[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return "unknown_person"
