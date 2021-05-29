# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import power
import serializeraw
import utila

import sections.feature.appendix


def appendix(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    source = power.link(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)

    dumped = sections.feature.appendix.work(text, textposition, pages=pages)
    assert dumped, dumped

    loaded = serializeraw.load_likelihood(dumped)
    return loaded


def test_appendix_diss170():
    extracted = appendix(power.DISS170_PDF)
    page163 = utila.select_page(extracted, 163)
    assert page163.content.value == 1.0
