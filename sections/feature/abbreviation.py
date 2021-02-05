# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Likelihood Detection
=================================

We search for selective headline "Abkuerzungsverzeichnis, ...".

NOTE: This approach is only for demo time.
"""

import iamraw
import serializeraw

import sections.feature
import sections.utils.headline

NO_PAGE = (0, 0)


def work(oneline_text: str, oneline_textpositions: str, pages=None) -> str:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        oneline_text,
        oneline_textpositions,
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
            content=iamraw.Likelihood(value, name='abbreviation_table'),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)

    dumped = serializeraw.dump_likelihood(result)
    return dumped


HEADLINES = [
    'Abbreviations',
    'Abbreviationtable',
    'Abkürzungen',
    'Abkürzungsverzeichnis',
]


def analyse_page(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        return NO_PAGE
    if isinstance(headlines, str):
        headlines = [headlines]
    for item in HEADLINES:
        if item in headlines:
            return 1, 1
    return NO_PAGE
