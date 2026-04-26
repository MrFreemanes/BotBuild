import os

from config.config import NAME_APP


def path_to_dir() -> str:
    """Путь к папке AppData/Roaming/{name} и ее создание."""
    appdata_path = os.getenv("APPDATA")
    dir_ = os.path.join(appdata_path, NAME_APP)
    return dir_


def path_to_logs() -> str:
    """Путь к папке logs."""
    log_dir = os.path.join(path_to_dir(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def path_to_logs_gui(name_file: str) -> str:
    """Путь к файлам .log в папке logs_gui."""
    gui_log_dir = os.path.join(path_to_logs(), "logs_gui")
    os.makedirs(gui_log_dir, exist_ok=True)
    return os.path.join(gui_log_dir, name_file)


def path_to_logs_core(name_file: str) -> str:
    """Путь к файлам .log в папке logs_core."""
    core_log_dir = os.path.join(path_to_logs(), "logs_core")
    os.makedirs(core_log_dir, exist_ok=True)
    return os.path.join(core_log_dir, name_file)


def path_to_bots(name_file: str) -> str:
    """Путь к файлам ботов в папке bots."""
    bots_dir = os.path.join(path_to_dir(), "bots")
    os.makedirs(bots_dir, exist_ok=True)
    return os.path.join(bots_dir, name_file)
