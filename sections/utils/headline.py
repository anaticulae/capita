# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import configo
import texmex
import utila


def headlines(navigator: texmex.PageTextNavigator):
    styles = common_textstyle(navigator[:])
    if not styles:
        return None

    # remove clusters with more than two items cause ?first? level are raw
    # on a single page.
    styles = [item for item in styles if len(item) <= 2]
    if not styles:
        return None
    # use hugest font size item
    maxsize = sorted(styles, key=lambda x: x.center.style.textsize())[-1]

    result = [item.text.strip() for item in maxsize]

    result = remove_numbered_pattern(result)

    if len(result) == 1:
        return result[0]
    return result


MAX_FONTSIZE_DIFF = configo.HV_PERCENT_PLUS(10).value


def common_textstyle(items, min_elements=1):

    def equal_fontsize(candidat, clusteritem):
        cluster = clusteritem.style.textsize()
        candidat = candidat.style.textsize()
        return pnear(cluster, candidat, rel_tol=MAX_FONTSIZE_DIFF)

    def classifier(candidat, clusteritem) -> bool:
        if not equal_fontsize(candidat, clusteritem):
            return False
        return True

    return utila.classifier.base.determine_cluster(
        items,
        classifier=classifier,
        min_elements=min_elements,
    )


def pnear(
        reference,
        current,
        rel_tol: float = 0.0,
        abs_tol: float = 0.05,
) -> bool:
    """\
    >>> pnear(10, 8, 0.2)
    True
    >>> pnear(10, 8, 0.19)
    False
    >>> pnear(0, 0.1, rel_tol=0.02, abs_tol=0.1)
    True
    """
    lower = reference * (1 - rel_tol)
    upper = reference * (1 + rel_tol)
    if lower <= current <= upper:
        return True
    lower = reference - abs_tol
    upper = reference + abs_tol
    if lower <= current <= upper:
        return True
    return False


# TODO: CODE DUPLICATION, COLLECT DIFFERENT HEADLINE PARSING APPROACHES
# AND CONVERT TO SINGLE ONE.
HEADLINE = re.compile(
    ('^'
     r'(?P<level>(\d{1,2}\.?)+\d{0,2})'
     r'[ ]{1,5}'
     r'(?P<text>.+?)'
     '$'),
    re.VERBOSE,
)


def parse_headline(line):
    line = line.strip()
    return re.match(HEADLINE, line)


def remove_numbered_pattern(items: list) -> list:
    """\
    >>> remove_numbered_pattern(['Anhang', '1.2.3 Content'])
    ['Anhang', 'Content']
    """
    result = []
    for item in items:
        parsed = parse_headline(item)
        if parsed:
            result.append(parsed['text'])
        else:
            result.append(item)
    return result
