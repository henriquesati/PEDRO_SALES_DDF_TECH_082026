"""
Subpacote de configurações e parâmetros declarativos dos geradores mock.
"""
from .constants import *
from .settings import VolumeConfig, AnomalyConfig, GeneratorSettings
from .profiles import load_profile, PROFILES, get_standard_profile, get_rich_profile, get_dev_profile
