# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


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


def load_plan(raw: str) -> list:
    raw = raw.strip()
    splitted = raw.splitlines()
    group = []
    for line in splitted:
        if not line.strip():
            continue
        if line[0] == '>':
            group.append((line[1:], []))
            continue
        line = line.strip()[1:]
        group[-1][1].append(line)
    return group
