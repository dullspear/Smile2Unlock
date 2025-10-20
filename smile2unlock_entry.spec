import os
import sys
from PyInstaller.utils.hooks import collect_data_files


# 在某些情况下（pyinstaller 执行 spec 时）__file__ 可能不存在（例如通过 runpy），使用 cwd/可执行路径作为回退
if getattr(sys, 'frozen', False):
    # frozen 下，使用 exe 所在目录作为 project root
    project_root = os.path.abspath(os.path.dirname(sys.executable))
else:
    # 非 frozen（构建/开发）时，使用 spec 文件所在目录（如果可用）或当前工作目录
    if '__file__' in globals():
        project_root = os.path.abspath(os.path.dirname(__file__))
    else:
        project_root = os.path.abspath(os.getcwd())

pathex = [project_root]

# 收集 face_recognition_models 包内的数据（如果安装在当前环境中）
face_models_datas = collect_data_files('face_recognition_models')

# 如果项目根目录下有 shape_predictor_68_face_landmarks.dat，则加入 datas
shape_predictor_path = os.path.join(project_root, 'shape_predictor_68_face_landmarks.dat')
shape_predictor_datas = [(shape_predictor_path, '.') ] if os.path.exists(shape_predictor_path) else []

# 递归收集 resources 文件夹内所有文件，保持相对目录结构
resources_dir = os.path.join(project_root, 'resources')
resources_datas = []
if os.path.isdir(resources_dir):
    for root, _, files in os.walk(resources_dir):
        rel_root = os.path.relpath(root, project_root)
        for fn in files:
            src = os.path.join(root, fn)
            # 目标路径为相对目录（在 exe 中保留 resources/... 结构）
            resources_datas.append((src, rel_root))

# 合并 datas（均为相对/项目内路径）
datas = face_models_datas + shape_predictor_datas + resources_datas

a = Analysis(
    ['smile2unlock_entry.py'],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=['face_recognition_models'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='smile2unlock_entry',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # 隐藏控制台窗口（双击 exe 不出现黑框）。若程序无法正确运行，清修改为 True 并重新编译。
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='smile2unlock_entry',
)
