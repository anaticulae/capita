# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

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
    if len(result) == 1:
        return result[0]
    return result


MAX_FONTSIZE_DIFF = 2.0  # TODO: HOLY VALUE


def common_textstyle(items, min_elements=1):

    def equal_fontsize(candidat, clusteritem):
        diff = math.fabs(candidat.style.textsize() -
                         clusteritem.style.textsize())
        return diff < MAX_FONTSIZE_DIFF

    def classifier(candidat, clusteritem) -> bool:
        if not equal_fontsize(candidat, clusteritem):
            return False
        return True

    return utila.classifier.base.determine_cluster(
        items,
        classifier=classifier,
        min_elements=min_elements,
    )
