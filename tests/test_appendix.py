# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import power
import serializeraw
import utila
import utilatest

import sections.feature.appendix


def appendix(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    source = power.link(source)
    utilatest.fixture_requires(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)

    dumped = sections.feature.appendix.work(text, textposition, pages=pages)
    assert dumped, dumped

    loaded = serializeraw.load_likelihood(dumped)
    return loaded


@utilatest.nightly
def test_appendix_diss170():
    extracted = appendix(power.DISS170_PDF)
    page163 = utila.select_page(extracted, 163)
    assert page163.content.value == 1.0


def test_appendix_diss143page121():
    """\
    Anhang A

    Frequenz- und Phasenselektive
    Messung sehr kleiner
    Signalamplituden
    """
    extracted = appendix(power.DISS143_PDF, pages=(121))
    page121 = utila.select_page(extracted, 121)
    assert page121.content.value == 1.0
