# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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


def test_abstract_diss180():
    extracted = abstract(power.DISS180_PDF, pages=(16,))
    page16 = utila.select_page(extracted, 16)
    assert page16.content.value == 1.0


def test_abtract_diss172():
    extracted = abstract(power.DISS172_PDF, pages=(3,))
    page3 = utila.select_page(extracted, 3)
    assert page3.content.value == 1.0


def test_abstract_master049():
    extracted = abstract(power.MASTER049_PDF, pages=(1,))
    page1 = utila.select_page(extracted, 1)
    assert page1.content.value == 1.0


def test_noabstract_bachelor111page14():
    """\
    2.2.4 Zusammenfassung was detected as abstract page.
    """
    extracted = abstract(power.BACHELOR111_PDF, pages=(14,))
    assert not extracted[0].content.value
