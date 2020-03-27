# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configparser
import dataclasses

import utila


@dataclasses.dataclass
class ExecutionPlan:
    config: dict = dataclasses.field(default_factory=dict)
    cmds: list = dataclasses.field(default_factory=list)


def dump_plan(plan: list, level=-1) -> str:
    result = []
    if isinstance(plan, list):
        for item in plan:
            result.append(dump_plan(item, level + 1))
    else:
        level = '    ' * level
        return level + '>' + plan
    joined = utila.NEWLINE.join(result)
    return joined + utila.NEWLINE


def load_plan(raw: str) -> ExecutionPlan:
    config, cmds = divide_plan(raw)
    config = load_config(config)
    cmds = load_cmds(cmds)
    return ExecutionPlan(config=config, cmds=cmds)


def divide_plan(raw):
    splitted = raw.splitlines()
    config, operation = [], []
    for line in splitted:
        if not line.strip():
            continue
        if line.strip()[0] == '>':
            operation.append(line)
        else:
            config.append(line)
    return utila.NEWLINE.join(config), utila.NEWLINE.join(operation)


def load_cmds(raw):
    group = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line[0] == '>':
            group.append((line[1:], []))
            continue
        line = line.strip()[1:]
        group[-1][1].append(line)
    return group


def load_config(raw: str, flat: bool = False) -> dict:
    r"""Load configuration from string.

    >>> load_config('[rawmaker]\nchar_margin = 10\nline_margin = 10.0')
    {'rawmaker': {'char_margin': '10', 'line_margin': '10.0'}}
    >>> load_config('first = 1\nsecond=2', flat=True)
    {'first': '1', 'second': '2'}
    """
    # TODO: MOVE TO UTILA
    config = configparser.ConfigParser(allow_no_value=True)
    try:
        config.read_string(raw)
    except configparser.MissingSectionHeaderError:
        # support formats without any section
        raw = f'[DEFAULT]\n{raw}'
        config.read_string(raw)

    result = {}
    for section, keys in config.items():
        level = {}
        for key in keys:
            level[key] = config[section][key]
        result[section] = level

    if flat:
        return result['DEFAULT']
    del result['DEFAULT']
    return result
