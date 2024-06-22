#!/usr/bin/env python
import os


def load_config():
    """
    Load a config class
    """

    mode = os.environ.get('MODE', 'DEV')
    print(mode)
    try:
        if mode == 'PRO':
            from .pro_config import ProConfig
            return ProConfig
        elif mode == 'DEV':
            from .dev_config import DevConfig
            return DevConfig
        elif mode == 'DETAIL1':
            print('\n\n')
            from .detail1_config import Detail1Config
            return Detail1Config
        elif mode == 'DETAIL2':
            from .detail2_config import Detail2Config
            return Detail2Config
        elif mode == 'DETAIL3':
            from .detail3_config import Detail3Config
            return Detail3Config
        elif mode == 'DETAIL4':
            from .detail4_config import Detail4Config
            return Detail4Config
        elif mode == 'DETAIL5':
            from .detail5_config import Detail5Config
            return Detail5Config
        else:
            from .dev_config import DevConfig
            return DevConfig
    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()