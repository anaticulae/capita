# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import statistics

import layout.double
import pdfinfo.pages
import utila


def detect_paper(pdf: str, pages: tuple = None) -> tuple:
    percents = layout.double.percentage(pdf, pages=pages)
    pages_max = pdfinfo.pages.determine(pdf)
    pages_gen = PageGenerator(pages=pages, pages_max=pages_max)
    grouped = group_percentage(percents, pages_gen=pages_gen)
    if not grouped:
        return None
    result = [(group[0][0], group[-1][0]) for group in grouped]
    result = merge_groups(result)
    return result


ROTATED = 'rotated'


def group_percentage(  # pylint:disable=R1260,R0912
    percents,
    pages_min: int = 6,
    double_column_min: float = 0.4,
    failure_max: int = 5,
    page_diff_max: int = 5,
    pages_gen: callable = None,
) -> list:
    """Determine connected group of pages.

    A. Finish group after 5 failures
    B. Include rotated pages into valid group
    C. Ensure that group is long enough

    Return a list of valid groups with pairs of (page, percent)
    """
    if not pages_gen:
        pages_gen = PageGenerator()
    failure = 0
    bonus = 0
    grouped = []
    for page, percent in zip(pages_gen, percents):
        density = []
        if isinstance(percent, tuple):
            percent, density = percent
        if failure and bonus % 3 == 0:  # pylint:disable=C2001
            failure -= 1
            bonus = 0
        # close group if failure count is too high
        if failure > failure_max:
            grouped.append([])
            failure = 0
            bonus = 0
        # close group if page distance is higher than `page_diff_max`
        if grouped and grouped[-1]:
            pagediff_error = (page - grouped[-1][-1][0]) > page_diff_max
        else:
            pagediff_error = False
        if pagediff_error:
            grouped.append([])
            failure = 0
            bonus = 0
        # decide if merging roated page to valid content before
        if percent == ROTATED:
            if pagediff_error:
                grouped.append([])
                failure = 0
                bonus = 0
            if grouped:
                grouped[-1].append((page, ROTATED))
            continue
        # double column rate is higher than requested rate
        success = percent is not None and percent > double_column_min
        density_mean = statistics.mean(density) if density else 0.0
        if density_mean < layout.strategy.DOUBLE_COLUMN_HIGH_DENSITY:
            # double page, but content is not dense enough. May an index
            # page and not a paper.
            success = False
        if not success:
            if grouped:
                failure += 1
                bonus = 0
            continue
        # merge valid to group before or create a new group
        if grouped:
            grouped[-1].append((page, percent))
        else:
            grouped.append([(page, percent)])
        if failure:
            bonus += 1
    # remove little groups
    grouped = [item for item in grouped if count_start(item) >= pages_min]
    return grouped


def count_start(items) -> int:
    """Ensure to have a valid, hight quality group start."""
    counted = 0
    for _, item in items:
        if item != ROTATED:
            counted += 1
        else:
            break
    return counted


def merge_groups(items, maxdiff: int = 5):
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        start, end = item
        if start - item[1] <= maxdiff:
            result[-1] = (result[-1][0], end)
        else:
            result.append(item)
    return result


class PageGenerator:
    """\
    >>> morepages = PageGenerator(pages_max=10)
    >>> (next(morepages), next(morepages), next(morepages))
    (0, 1, 2)
    >>> [next(morepages) for _ in range(5)]
    [3, 4, 5, 6, 7]
    """

    def __init__(self, pages: tuple = None, pages_max: int = 256):
        self.pages = [
            page for page in utila.rlist(pages_max)
            if not utila.should_skip(page, pages)
        ]
        self.pages = iter(self.pages)

    def __iter__(self):
        return self.pages

    def __next__(self):
        return next(self.pages)
