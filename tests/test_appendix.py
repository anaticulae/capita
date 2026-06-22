# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita.feature.appendix
import hoverpower
import iamraw
import iamraw.path
import serializeraw
import utilo
import utilotest


def appendix(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    source = hoverpower.link(source)
    utilotest.fixture_requires(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)

    dumped = capita.feature.appendix.work(text, textposition, pages=pages)
    assert dumped, dumped

    loaded = serializeraw.load_likelihood(dumped)
    return loaded


@utilotest.nightly
def test_appendix_diss170():
    extracted = appendix(hoverpower.DISS170_PDF)
    page163 = utilo.select_page(extracted, 163)
    assert page163.content.value == 1.0


def test_appendix_diss143page121():
    """\
    Anhang A

    Frequenz- und Phasenselektive
    Messung sehr kleiner
    Signalamplituden
    """
    extracted = appendix(hoverpower.DISS143_PDF, pages=(121,))
    page121 = utilo.select_page(extracted, 121)
    assert page121.content.value == 1.0
