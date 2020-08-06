# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Appendix Detector
=================
"""

import iamraw
import serializeraw

import sections.feature
import sections.utils.headline

NO_PAGE = (0, 0)


def work(text_linewise: str, textpositions: str, pages: tuple = None) -> str:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text_linewise,
        textpositions,
        pages=pages,
    )

    result = {page.page: analyse_page(page) for page in navigators}

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


HEADLINES = [
    'Anhang',
    'A. Anhang',
    'Anhang A',
    'Anhang B',
    'Anhang C',
    'Anhang D',
]


def analyse_page(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        return NO_PAGE
    if isinstance(headlines, str):
        headlines = [headlines]

    # ensure that every cased headlines are parsed correctly
    headlines = lower(headlines)
    for item in lower(HEADLINES):
        if item in headlines:
            return 1, 1
    return NO_PAGE


# TODO: MOVE TO UTILA
def lower(items):
    return [item.lower() for item in items]
