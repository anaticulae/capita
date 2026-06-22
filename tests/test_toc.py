# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import pytest
import serializeraw
import utilo
import utilotest

import capita.feature.toc
import capita.strategy
import capita.table

DOCU27 = hoverpower.link(hoverpower.DOCU027_PDF)


@utilotest.requires(hoverpower.DOCU027_PDF)
def test_extract_toc_likelihood():
    navigator = serializeraw.ptn_frompath(DOCU27)
    extracted = capita.strategy.extract_xxx_likelihood(
        navigator,
        'Contents',
        pattern=capita.table.valid_line,
    )
    extracted = [item.content.value for item in extracted]
    assert sum(extracted) == pytest.approx(1.0)


@utilotest.requires(hoverpower.BACHELOR063_PDF)
def test_extract_toc_likelihood_bachelor63():
    text = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.BACHELOR063_PDF),
        pages=utilo.rtuple(8),
        prefix='oneline',
    )
    extracted = capita.strategy.extract_xxx_likelihood(
        text,
        headline='Inhaltsverzeichnis',
        pattern=capita.table.valid_line,
    )
    extracted = [item.content.value for item in extracted]
    likelihood = sum(extracted)
    # table of content is spreaded over two pages. Therefore the
    # likelihood must be higher than 1.0
    assert likelihood >= 1.0, str(likelihood)  # holy value


@utilotest.requires(hoverpower.MASTER072_PDF)
def test_extract_toc_likelihood_master72():
    """Check that only second and third page are detected as toc.
    Repeating the strategy due `without` is required to discover
    complete table of content."""
    text = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.MASTER072_PDF),
        pages=utilo.rtuple(8),
        prefix='oneline',
    )
    extracted = capita.strategy.extract_xxx_likelihood(
        text,
        headline='Inhaltsverzeichnis',
        pattern=capita.table.valid_line,
    )
    without = capita.strategy.extract_xxx_likelihood(
        text,
        headline=None,
        pattern=capita.table.valid_line,
    )
    extracted = capita.strategy.merge_second(extracted, without)
    extracted = [item.content.value for item in extracted]

    expected_result = [False, True, True, False, False, False, False, False]
    for page, (current, expected) in enumerate(zip(extracted, expected_result)):
        if expected:
            assert current > 0.75, f'page {page} value: {current}'
        else:
            assert current < 0.05, f'page: {page} value: {current}'


def extract_toc(
    source: str,
    pages: tuple = None,
) -> iamraw.PageContentLikelihoods:
    utilotest.fixture_requires(source)
    text = iamraw.path.text(source, prefix='oneline')
    textposition = iamraw.path.textposition(source, prefix='oneline')
    sizeandborder = iamraw.path.sizeandborder(source)
    headerfooters = iamraw.path.headerfooters(source)
    dumped = capita.feature.toc.work(
        oneline_text=text,
        oneline_textposition=textposition,
        sizeandborder=sizeandborder,
        headerfooters=headerfooters,
        pages=pages,
    )
    assert dumped, dumped
    loaded = serializeraw.load_likelihood(dumped)
    return loaded


# DISS266 VALIDATED!
@utilotest.longrun
@pytest.mark.parametrize('source, expected', [
    pytest.param(hoverpower.DISS266_PDF, [4, 5, 6], id='diss266'),
    pytest.param(hoverpower.ORDER107_PDF, [2], id='order107'),
    pytest.param(hoverpower.MASTER155_PDF, [1, 2], id='master155'),
    pytest.param(hoverpower.MASTER091A_PDF, [3, 4], id='master91a'),
    pytest.param(hoverpower.DISS172_PDF, [7, 8], id='diss172'),
    pytest.param(hoverpower.DISS406_PDF, utilo.rlist(3, 12), id='diss406'),
    pytest.param(hoverpower.BOOK173_PDF, [9, 10, 11, 12], id='book173'),
])
def test_toc_extract(source, expected):
    source = hoverpower.link(source)
    # run
    result = extract_toc(
        source=source,
        pages=utilo.rtuple(15),
    )
    # verify result
    pages = [item.page for item in result if item.content.value]
    assert pages == expected
