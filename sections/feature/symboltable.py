# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abstract Detector
=================
"""

import iamraw
import serializeraw
import utila

import sections.feature
import sections.utils.headline


def work(text_linewise: str, textpositions: str, pages=None) -> str:
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
            content=iamraw.Likelihood(value, name='symboltable'),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)

    dumped = serializeraw.dump_likelihood(result)
    return dumped


HEADLINES_SYMBOLTABLE = utila.splitlines("""
SYMBOL
SYMBOLS
SYMBOLVERZEICHNIS
""")


def analyse_page(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        return sections.feature.NO_PAGE
    if utila.similar(
            expected=HEADLINES_SYMBOLTABLE,
            current=headlines,
            maxdiff=0.95,
    ):
        return sections.feature.PERFECT
    return sections.feature.NO_PAGE
