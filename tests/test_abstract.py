# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilo
import utilotest

import sections.feature.abstract


def abstract(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    source = hoverpower.link(source)
    utilotest.fixture_requires(source)
    dumped = sections.feature.abstract.work(
        source,
        source,
        source,
        source,
        source,
        pages=pages,
    )
    assert dumped, dumped
    loaded = serializeraw.load_likelihood(dumped)
    return loaded


def test_abstract_diss180():
    extracted = abstract(hoverpower.DISS180_PDF, pages=(16,))
    page16 = utilo.select_page(extracted, 16)
    assert page16.content.value == 1.0


def test_abtract_diss172():
    extracted = abstract(hoverpower.DISS172_PDF, pages=(3,))
    page3 = utilo.select_page(extracted, 3)
    assert page3.content.value == 1.0


def test_abstract_master049():
    extracted = abstract(hoverpower.MASTER049_PDF, pages=(1,))
    page1 = utilo.select_page(extracted, 1)
    assert page1.content.value == 1.0


@utilotest.longrun
def test_abstract_master193():
    extracted = abstract(hoverpower.MASTER193_PDF, pages=(191, 192))
    page191 = utilo.select_page(extracted, 191)
    assert page191.content.value == 1.0
    page192 = utilo.select_page(extracted, 192)
    assert page192.content.value == 1.0


@utilotest.longrun
def test_noabstract_bachelor111page14():
    """\
    2.2.4 Zusammenfassung was detected as abstract page.
    """
    extracted = abstract(hoverpower.BACHELOR111_PDF, pages=(14,))
    assert not extracted[0].content.value
