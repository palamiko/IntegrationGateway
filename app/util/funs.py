import os
import sys
import yaml

from app.dto.priority_enum import PriorityEnumZD, PriorityEnumJira


def mapping_priority(priority: PriorityEnumZD):
    match priority:
        case PriorityEnumZD.low:
            return PriorityEnumJira.standard

        case PriorityEnumZD.normal:
            return PriorityEnumJira.medium

        case PriorityEnumZD.urgent:
            return PriorityEnumJira.high

        case PriorityEnumZD.extra:
            return PriorityEnumJira.crit


def detect_os() -> str:
    if sys.platform.startswith('win32'):
        return ".\\log_conf.yaml"
    else:
        return "./log_conf.yaml"


def get_log_conf(default_path=detect_os(), env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
            return config


