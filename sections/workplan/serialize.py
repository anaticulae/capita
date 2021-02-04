# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import utila


@dataclasses.dataclass
class ExecutionPlan:
    config: dict = dataclasses.field(default_factory=dict)
    cmds: list = dataclasses.field(default_factory=list)


def dump_plan(plan: ExecutionPlan) -> str:
    assert isinstance(plan, ExecutionPlan), type(plan)
    header = utila.dump_config(plan.config)
    tailer = dump_cmds(plan.cmds)
    return f'{header}\n{tailer}'


def load_plan(raw: str) -> ExecutionPlan:
    config, cmds = divide_plan(raw)
    config = utila.load_config(config)
    cmds = load_cmds(cmds)
    return ExecutionPlan(config=config, cmds=cmds)


def divide_plan(raw: str):
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


def dump_cmds(plan: list, level: int = -1) -> str:
    result = []
    if isinstance(plan, list):
        for item in plan:
            result.append(dump_cmds(item, level + 1))
    else:
        level = '    ' * level
        return level + '>' + plan
    joined = utila.NEWLINE.join(result)
    return joined + utila.NEWLINE


def load_cmds(raw: str) -> list:
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
