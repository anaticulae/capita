# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elementae.headline.lookup
import serializeraw
import utilo

import capita.feature
import capita.utils.headline


def work(oneline_text: str, oneline_textpositions: str, pages=None) -> str:
    navigators = serializeraw.ptn_fromfile(
        oneline_text,
        oneline_textpositions,
        pages=pages,
    )
    result = capita.feature.pagebypage(
        navigators,
        analyse_page,
        name='acknowledge',
    )

    dumped = serializeraw.dump_likelihood(result)
    return dumped


def analyse_page(content):
    headlines = capita.utils.headline.headlines(content)
    if not headlines:
        return capita.feature.NO_PAGE
    if utilo.similar(
            expected=elementae.headline.lookup.ACKNOWLEDGE,
            current=headlines,
            maxdiff=0.95,
    ):
        return capita.feature.PERFECT
    return capita.feature.NO_PAGE
