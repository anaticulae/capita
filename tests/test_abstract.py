# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import sections.feature.abstract


def abstract(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    source = power.link(source)
    utilatest.fixture_requires(source)
    dumped = sections.feature.abstract.work(
        source,
        source,
        source,
        source,
        pages=pages,
    )
    assert dumped, dumped
    loaded = serializeraw.load_likelihood(dumped)
    return loaded


def test_appendix_diss180():
    extracted = abstract(power.DISS180_PDF, pages=(16,))
    page16 = utila.select_page(extracted, 16)
    assert page16.content.value == 1.0
