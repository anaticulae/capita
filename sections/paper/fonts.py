# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import texmex


def bypage(navigators: texmex.PageTextNavigators):
    result = []
    for page in navigators:
        parsed = parse_page(page)
        result.append(parsed)
    return result


def parse_page(navigator: texmex.PageTextNavigator):
    fontsize = collections.defaultdict(int)
    fontface = collections.defaultdict(int)
    for line in navigator:
        for style in line.style.content:
            width = (style.end - style.start)
            fontsize[style.size] += width
            fontface[style.font] += width
    fontsize, fontface = dict(fontsize), dict(fontface)
    return fontsize, fontface
