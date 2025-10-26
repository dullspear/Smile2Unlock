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

# ============== generate_db 分析和打包 ==============
a_generate_db = Analysis(
    ['generate_db.py'],
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
pyz_generate_db = PYZ(a_generate_db.pure)

exe_generate_db = EXE(
    pyz_generate_db,
    a_generate_db.scripts,
    [],
    exclude_binaries=True,
    name='generate_db',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # 隐藏控制台窗口（双击 exe 不出现黑框）。若程序无法正确运行，清修改为 True 并重新编译，以方便观察输出。
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ============== smile2unlock_entry 分析和打包 ==============
a_smile2unlock = Analysis(
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
pyz_smile2unlock = PYZ(a_smile2unlock.pure)

exe_smile2unlock = EXE(
    pyz_smile2unlock,
    a_smile2unlock.scripts,
    [],
    exclude_binaries=True,
    name='smile2unlock_entry',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # 隐藏控制台窗口（双击 exe 不出现黑框）。若程序无法正确运行，清修改为 True 并重新编译，以方便观察输出。
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ============== 合并收集所有文件到同一目录 ==============
coll = COLLECT(
    exe_generate_db,
    a_generate_db.binaries,
    a_generate_db.datas,
    exe_smile2unlock,
    a_smile2unlock.binaries,
    a_smile2unlock.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Smile2Unlock',
)