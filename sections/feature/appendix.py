# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Appendix Detector
=================
"""

import iamraw
import serializeraw
import utila

import sections.feature
import sections.utils.headline

NO_PAGE = (0, 0)


def work(text_linewise: str, textpositions: str, pages: tuple = None) -> str:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text_linewise,
        textpositions,
        pages=pages,
    )

    # TODO: MAY CHANGE LATER?
    # do not detect appendix at the start of the document
    minpage = len(navigators) * 0.3
    result = {
        page.page: analyse_page(page) if page.page > minpage else NO_PAGE
        for page in navigators
    }

    uniformed = sections.feature.uniform_result(result)
    multiformed = sections.feature.multiform_result(result)
    if multiformed is not None:
        uniformed = multiformed
    assert len(uniformed) == len(navigators)

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, name='appendix'),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)

    dumped = serializeraw.dump_likelihood(result)
    return dumped


def analyse_page(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        return NO_PAGE
    # ensure that every cased headlines are parsed correctly
    if utila.similar(expected=HEADLINES, current=headlines, maxdiff=0.9):
        return 1, 1
    return NO_PAGE


HEADLINES = utila.splitlines("""
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
