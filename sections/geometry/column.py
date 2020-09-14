# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

# TODO: MOVE TO HEY PROJECT


def parse(navigator, column_elements_min=10) -> list:
    # TODO: ADD PARAMETER TO SELECT REQUESTED COLUMN COUNT
    marker = columns(navigator, min_elements=column_elements_min)
    if not marker:
        return None

    if len(marker) > 2:
        utila.debug(f'more than 2 marker: {len(marker)} page: {navigator.page}')
        utila.debug('skip column extraction')
        return None

    firstcolumn, secondcolumn = split_bymarker(navigator, marker)

    overlapping = overlapping_column(firstcolumn, secondcolumn)
    if overlapping:
        # TODO: EXTEND ERROR MESSAGE
        utila.debug(overlapping)
        utila.debug('could not analyze, columns are mixed/ambigous')
        return None

    return firstcolumn, secondcolumn


def split_bymarker(page, marker):
    if not marker:
        return None
    firstmarker = marker[0]
    secondmarker = marker[1]
    firstcolumn = column_data(page, firstmarker)
    secondcolumn = column_data(page, secondmarker)
    return [firstcolumn, secondcolumn]


def overlapping_column(short, description):
    # TODO: INTRODUCE HASH BOUNDING METHOD
    shorts = set(str(item.bounding) for item in short)
    descriptions = set(str(item.bounding) for item in description)

    mixig = shorts & descriptions
    return mixig


def column_data(page, x0, diff: float = 60.0):
    """Filter items by x0 coordinate. Find items which are on a vertical
    line."""
    result = []
    for item in page:
        if not utila.near(item.bounding[0], x0, diff):
            continue
        result.append(item)
    return result


def columns(page, min_elements) -> utila.Numbers:
    """Sort columns from left to right."""
    collected = []
    for item in page:
        x0 = item.bounding[0]
        collected.append(x0)

    # High diff to join alternating text start to a single text start
    clustered = utila.max_distance(
        collected,
        diff=50,  # TODO: HOLY VALUE
        min_elements=min_elements  # TODO: HOLY VALUE
    )
    if len(clustered) < 2:
        return None

    result = [item[0] for item in clustered]
    result = sorted(result)
    return result
