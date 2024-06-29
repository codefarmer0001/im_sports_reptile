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
        elif mode == 'm1':
            from .main1_config import Main1Config
            return Main1Config
        elif mode == 'm2':
            from .main2_config import Main2Config
            return Main2Config
        elif mode == 'm3':
            from .main3_config import Main3Config
            return Main3Config
        elif mode == 'd1':
            print('\n\n')
            from .detail1_config import Detail1Config
            return Detail1Config
        elif mode == 'd2':
            from .detail2_config import Detail2Config
            return Detail2Config
        elif mode == 'd3':
            from .detail3_config import Detail3Config
            return Detail3Config
        elif mode == 'd4':
            from .detail4_config import Detail4Config
            return Detail4Config
        elif mode == 'd5':
            from .detail5_config import Detail5Config
            return Detail5Config
        elif mode == 'd6':
            from .detail6_config import Detail6Config
            return Detail6Config
        elif mode == 'd7':
            from .detail7_config import Detail7Config
            return Detail7Config
        elif mode == 'd8':
            from .detail8_config import Detail8Config
            return Detail8Config
        elif mode == 'd9':
            from .detail9_config import Detail9Config
            return Detail9Config
        elif mode == 'd10':
            from .detail10_config import Detail10Config
            return Detail10Config
        else:
            from .main1_config import Main1Config
            return Main1Config
    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()