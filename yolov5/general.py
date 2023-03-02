import os
import platform
from pathlib import Path

# @TryExcept()
# def check_requirements(requirements=ROOT / 'requirements.txt', exclude=(), install=True, cmds=''):
#     # Check installed dependencies meet YOLOv5 requirements (pass *.txt file or list of packages or single package str)
#     prefix = colorstr('red', 'bold', 'requirements:')
#     check_python()  # check python version
#     if isinstance(requirements, Path):  # requirements.txt file
#         file = requirements.resolve()
#         assert file.exists(), f"{prefix} {file} not found, check failed."
#         with file.open() as f:
#             requirements = [f'{x.name}{x.specifier}' for x in pkg.parse_requirements(f) if x.name not in exclude]
#     elif isinstance(requirements, str):
#         requirements = [requirements]

#     s = ''
#     n = 0
#     for r in requirements:
#         try:
#             pkg.require(r)
#         except (pkg.VersionConflict, pkg.DistributionNotFound):  # exception if requirements not met
#             s += f'"{r}" '
#             n += 1

#     if s and install and AUTOINSTALL:  # check environment variable
#         LOGGER.info(f"{prefix} YOLOv5 requirement{'s' * (n > 1)} {s}not found, attempting AutoUpdate...")
#         try:
#             # assert check_online(), "AutoUpdate skipped (offline)"
#             LOGGER.info(check_output(f'pip install {s} {cmds}', shell=True).decode())
#             source = file if 'file' in locals() else requirements
#             s = f"{prefix} {n} package{'s' * (n > 1)} updated per {source}\n" \
#                 f"{prefix} ⚠️ {colorstr('bold', 'Restart runtime or rerun command for updates to take effect')}\n"
#             LOGGER.info(s)
#         except Exception as e:
#             LOGGER.warning(f'{prefix} ❌ {e}')

def is_writeable(dir, test=False):
    # Return True if directory has write permissions, test opening a file with write permissions if test=True
    if not test:
        return os.access(dir, os.W_OK)  # possible issues on Windows
    file = Path(dir) / 'tmp.txt'
    try:
        with open(file, 'w'):  # open file with write permissions
            pass
        file.unlink()  # remove file
        return True
    except OSError:
        return False
    
def user_config_dir(dir='Ultralytics', env_var='YOLOV5_CONFIG_DIR'):
    # Return path of user configuration directory. Prefer environment variable if exists. Make dir if required.
    env = os.getenv(env_var)
    if env:
        path = Path(env)  # use environment variable
    else:
        cfg = {'Windows': 'AppData/Roaming', 'Linux': '.config', 'Darwin': 'Library/Application Support'}  # 3 OS dirs
        path = Path.home() / cfg.get(platform.system(), '')  # OS-specific config dir
        path = (path if is_writeable(path) else Path('/tmp')) / dir  # GCP and AWS lambda fix, only /tmp is writeable
    path.mkdir(exist_ok=True)  # make if required
    return path


CONFIG_DIR = user_config_dir()  # Ultralytics settings dir
FONT = 'Arial.ttf'  # https://ultralytics.com/assets/Arial.ttf
