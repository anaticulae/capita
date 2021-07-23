# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> group_percentage([0.0, 0.0, 0.0, 0.61, 0.4, 0.39, 0.72, 0.0, None, 0.39,
... 0.0, None, 0.83, 'rotated', 'rotated', 'rotated', 'rotated', 'rotated',
... 'rotated', 'rotated', 0.8])
[]
"""

import sections.paper.layout


def detect_paper(pdf: str) -> tuple:
    percents = sections.paper.layout.percentage(pdf)
    grouped = group_percentage(percents)
    if not grouped:
        return None
    result = [(group[0][0], group[-1][0]) for group in grouped]
    return result


def group_percentage(
    percents,
    pages_min: int = 6,
    double_column_min: float = 0.4,
) -> list:
    """Determine connected group of pages.

    A. Finish group after 5 failures
    B. Include rotated pages into valid group
    C. Ensure that group is long enough

    Return a list of valid groups with pairs of (page, percent)
    """
    failure = 0
    grouped = []
    for page, percent in enumerate(percents):
        if failure > 5:
            grouped.append([])
            failure = 0
        if percent == 'rotated':
            if grouped:
                grouped[-1].append((page, 'rotated'))
            continue
        success = percent is not None and percent > double_column_min
        if not success:
            if grouped:
                failure += 1
            continue
        if grouped:
            grouped[-1].append((page, percent))
        else:
            grouped.append([(page, percent)])
    # remove little groups
    grouped = [item for item in grouped if count_start(item) >= pages_min]
    return grouped


def count_start(items):
    """Ensure to have a valid, hight quality group start."""
    counted = 0
    for _, item in items:
        if item != 'rotated':
            counted += 1
        else:
            break
    return counted
