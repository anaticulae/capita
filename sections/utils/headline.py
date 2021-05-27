# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import configo
import elements
import texmex
import utila


def headlines(
    navigator: texmex.PageTextNavigator,
    min_length: int = 5,  # TODO: HOLY VALUE
    # max_length: int = 50,  # TODO: HOLY VALUE
    min_word_count: int = 1,
    max_word_count: int = 3,
    topsearch: bool = False,
):
    """\
    #topsearch: use upper area of page
    """

    navigator = navigator[0:6] if topsearch else navigator[:]
    navigator = [
        item for item in navigator if not elements.noheadline(
            line=item.text,
            length_min=min_length,
            wordcount_max=max_word_count,
        )
    ]

    styles = common_textstyle(navigator)
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
    # remove to many spaces
    result = [
        item for item in result
        if min_word_count <= len(item.split()) <= max_word_count
    ]
    result = [item.title() for item in result]
    result = remove_numbered_pattern(result)

    if len(result) == 1:
        return result[0]
    return result


MAX_FONTSIZE_DIFF = configo.HV_PERCENT_PLUS(10).value


def common_textstyle(items, min_elements=1):

    def equal_fontsize(candidat, clusteritem):
        cluster = clusteritem.style.textsize()
        candidat = candidat.style.textsize()
        return utila.pnear(cluster, candidat, rel_tol=MAX_FONTSIZE_DIFF)

    def classifier(candidat, clusteritem) -> bool:
        if not equal_fontsize(candidat, clusteritem):
            return False
        return True

    return utila.classifier.base.determine_cluster(
        items,
        classifier=classifier,
        min_elements=min_elements,
    )


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
