# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Appendix Detector
=================
"""

import capita.feature
import capita.utils.headline
import serializeraw
import utilo


def work(text_linewise: str, textpositions: str, pages: tuple = None) -> str:
    navigators = serializeraw.ptn_fromfile(
        text_linewise,
        textpositions,
        pages=pages,
    )
    # TODO: MAY CHANGE LATER?
    # do not detect appendix at the start of the document
    result = capita.feature.pagebypage(
        navigators=navigators,
        pageme=analyse_page,
        name='appendix',
        minpage=0.3 * len(navigators),
    )
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def analyse_page(content):
    headlines = capita.utils.headline.headlines(content)
    if not headlines:
        return capita.feature.NO_PAGE
    # ensure that every cased headlines are parsed correctly
    if utilo.similar(expected=HEADLINES, current=headlines, maxdiff=0.9):
        return capita.feature.PERFECT
    return capita.feature.NO_PAGE


HEADLINES = utilo.splitlines("""
A. Anhang
B. Anhang
C. Anhang
D. Anhang
Anhang 1
Anhang 2
Anhang 3
Anhang 4
Anhang 5
Anhang 6
Anhang 7
Anhang 8
Anhang 9
Anhang 10
Anhang A
Anhang B
Anhang C
Anhang D
Anhang
Anhangsverzeichnis
Appendix
I Anhang
II Anhang
III Anhang
IIII Anhang
IV Anhang
V Anhang
VI Anhang
VII Anhang
VIII Anhang
""")
