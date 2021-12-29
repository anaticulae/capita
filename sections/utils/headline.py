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

HEADLINES_LENGTH_MIN = configo.HV_INT_PLUS(default=5)

HEADLINES_WORD_COUNT_MIN = configo.HV_INT_PLUS(default=1)

HEADLINES_WORD_COUNT_MAX = configo.HV_INT_PLUS(default=5)


def headlines(
    navigator: texmex.PageTextNavigator,
    length_min: int = HEADLINES_LENGTH_MIN,
    # max_length: int = 50,
    word_count_min: int = HEADLINES_WORD_COUNT_MIN,
    word_count_max: int = HEADLINES_WORD_COUNT_MAX,
    topsearch: bool = False,
    level_max: int = None,
):
    """\
    #topsearch: use upper area of page
    """
    navigator = navigator[0:6] if topsearch else navigator[:]
    navigator = [
        item for item in navigator if not elements.noheadline(
            line=item.text,
            length_min=length_min,
            wordcount_max=word_count_max,
        )
    ]
    styles = common_textstyle(navigator)
    if not styles:
        if backup := headline_lookup(navigator):
            return backup
        return None
    styles = cleanup_styles(styles)
    if not styles:
        if backup := headline_lookup(navigator):
            return backup
        return None
    # use hugest font size item
    maxsize = sorted(styles, key=lambda x: x.center.style.textsize())[-1]
    result = [item.text.strip() for item in maxsize]
    # remove to many spaces
    result = [
        item for item in result
        if word_count_min <= len(item.split()) <= word_count_max or
        elements.headline.decide.singlechar(item)
    ]
    result = [item.title() for item in result]
    result = remove_numbered_pattern(result, level_max=level_max)
    if len(result) == 1:
        return result[0]
    return result


def headline_lookup(ptn):
    """Backup strategy."""
    result = []
    for line in ptn[0:4]:
        if not elements.isheadline(line.text):
            continue
        result.append(line.text)
    return result


def cleanup_styles(styles):
    """Remove clusters with more than two items cause ?first? level are

    raw on a single page.
    """
    result = []
    for cluster in styles:
        fontsize = cluster.center.style.textsize()
        if fontsize > 20:
            result.append(cluster)
            continue
        if fontsize > 15:
            result.append(cluster)
            continue
        if len(cluster) > 2:
            # too many elements for small font size
            continue
        result.append(cluster)
    return result


FONTSIZE_DIFF_MAX = configo.HV_PERCENT_PLUS(default=10)


def common_textstyle(items, elements_min=1):

    def equal_fontsize(candidat, clusteritem):
        cluster = clusteritem.style.textsize()
        candidat = candidat.style.textsize()
        return utila.pnear(cluster, candidat, rel_tol=FONTSIZE_DIFF_MAX)

    def classifier(candidat, clusteritem) -> bool:
        if not equal_fontsize(candidat, clusteritem):
            return False
        return True

    return utila.classifier.base.determine_cluster(
        items,
        classifier=classifier,
        min_elements=elements_min,
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


def remove_numbered_pattern(items: list, level_max: int = None) -> list:
    """\
    >>> remove_numbered_pattern(['Anhang', '1.2.3 Content'])
    ['Anhang', 'Content']
    """
    result = []
    for item in items:
        parsed = parse_headline(item)
        if parsed:
            if level_max is not None:
                level = elements.level_numbered(parsed['level'])
                if level > level_max:
                    continue
            result.append(parsed['text'])
        else:
            result.append(item)
    return result
