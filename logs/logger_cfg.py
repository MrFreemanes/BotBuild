from utils.paths import path_to_logs_gui, path_to_logs_core

cfg = {
    'version': 1,
    'formatters': {
        'console_msg': {
            'format': '%(asctime)s | %(levelname)7s | %(filename)s:%(funcName)s:%(lineno)s | %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'file_msg': {
            'format': '%(asctime)s | %(levelname)7s | %(filename)s:%(funcName)s:%(lineno)s | %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console_msg'
        },
        'file_main': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_core("main.log"),
            'formatter': 'file_msg',
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 5,  # хранить 5 старых файлов
            'encoding': 'utf-8'
        },
        'file_window': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_gui("window.log"),
            'formatter': 'file_msg',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_bridge': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_gui("bridge.log"),
            'formatter': 'file_msg',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_worker_Worker': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_core("Worker.log"),
            'formatter': 'file_msg',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_model': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_gui("model.log"),
            'formatter': 'file_msg',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_widget': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_gui("widget.log"),
            'formatter': 'file_msg',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_graph_view': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_logs_gui("graph_view.log"),
            'formatter': 'file_msg',
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        'log_main': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_main'],
            'propagate': False
        },
        'log_window': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_window'],
            'propagate': False
        },
        'log_bridge': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_bridge'],
            'propagate': False
        },
        'log_worker_Worker': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_worker_Worker'],
            'propagate': False
        },
        'log_model': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_model'],
            'propagate': False
        },
        'log_widget': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_widget'],
            'propagate': False
        },
        'log_graph_view': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_graph_view'],
            'propagate': False
        },
    }
}
