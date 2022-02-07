# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import sections.feature.toc
import sections.strategy
import sections.table

DOCU27 = power.link(power.DOCU027_PDF)


@utilatest.requires(power.DOCU027_PDF)
def test_extract_toc_likelihood():
    navigator = serializeraw.create_pagetextnavigators_frompath(DOCU27)
    extracted = sections.strategy.extract_xxx_likelihood(
        navigator,
        'Contents',
        pattern=sections.table.valid_line,
    )
    extracted = [item.content.value for item in extracted]
    assert sum(extracted) == pytest.approx(1.0)


@utilatest.requires(power.BACHELOR063_PDF)
def test_extract_toc_likelihood_bachelor63():
    text = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR063_PDF),
        pages=utila.ranged_tuple(0, 8),
        prefix='oneline',
    )
    extracted = sections.strategy.extract_xxx_likelihood(
        text,
        headline='Inhaltsverzeichnis',
        pattern=sections.table.valid_line,
    )
    extracted = [item.content.value for item in extracted]
    likelihood = sum(extracted)
    # table of content is spreaded over two pages. Therefore the
    # likelihood must be higher than 1.0
    assert likelihood >= 1.0, str(likelihood)  # holy value


@utilatest.requires(power.MASTER072_PDF)
def test_extract_toc_likelihood_master72():
    """Check that only second and third page are detected as toc.
    Repeating the strategy due `without` is required to discover
    complete table of content."""
    text = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.MASTER072_PDF),
        pages=utila.ranged_tuple(0, 8),
        prefix='oneline',
    )
    extracted = sections.strategy.extract_xxx_likelihood(
        text,
        headline='Inhaltsverzeichnis',
        pattern=sections.table.valid_line,
    )
    without = sections.strategy.extract_xxx_likelihood(
        text,
        headline=None,
        pattern=sections.table.valid_line,
    )
    extracted = sections.strategy.merge_second(extracted, without)
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
    utilatest.fixture_requires(source)
    text = iamraw.path.text(source, prefix='oneline')
    textposition = iamraw.path.textposition(source, prefix='oneline')
    sizeandborder = iamraw.path.sizeandborder(source)
    headerfooters = iamraw.path.headerfooters(source)
    dumped = sections.feature.toc.work(
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
@pytest.mark.parametrize('source, expected', [
    pytest.param(power.DISS266_PDF, [4, 5, 6], id='diss266'),
    pytest.param(power.ORDER107_PDF, [2], id='order107'),
    pytest.param(power.MASTER155_PDF, [1, 2], id='master155'),
    pytest.param(power.MASTER091A_PDF, [3, 4], id='master91a'),
    pytest.param(power.DISS172_PDF, [7, 8], id='diss172'),
    pytest.param(power.DISS406_PDF, utila.ranged_list(3, 12), id='diss406'),
    pytest.param(power.BOOK173_PDF, [9, 10, 11, 12], id='book173'),
])
@utilatest.longrun
def test_toc_extract(source, expected):
    source = power.link(source)
    # run
    result = extract_toc(
        source=source,
        pages=utila.ranged_tuple(0, 15),
    )
    # verify result
    pages = [item.page for item in result if item.content.value]
    assert pages == expected
