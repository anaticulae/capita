# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila

import sections.feature.toc
import sections.table.strategy

DOCU27 = power.link(power.DOCU27_PDF)


#pylint:disable=W0621
def test_extract_toc_likelihood():
    navigator = serializeraw.create_pagetextnavigators_frompath(DOCU27)
    extracted = sections.table.strategy.extract_xxx_likelihood(navigator)
    extracted = [item.content.value for item in extracted]
    assert sum(extracted) == pytest.approx(1.0)


def test_extract_toc_likelihood_bachelor63():
    text = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR063_PDF),
        pages=utila.ranged_tuple(0, 8),
        prefix='oneline',
    )
    extracted = sections.table.strategy.extract_xxx_likelihood(
        text,
        headline='Inhaltsverzeichnis',
    )
    extracted = [item.content.value for item in extracted]
    likelihood = sum(extracted)
    # table of content is spreaded over two pages. Therefore the
    # likelihood must be higher than 1.0
    assert likelihood > 1.5, str(likelihood)  # holy value


def test_extract_toc_likelihood_master72():
    """Check that only second and third page are detected as table of content."""
    text = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.MASTER072_PDF),
        pages=utila.ranged_tuple(0, 8),
        prefix='oneline',
    )
    extracted = sections.table.strategy.extract_xxx_likelihood(
        text,
        headline='Inhaltsverzeichnis',
    )
    extracted = [item.content.value for item in extracted]

    expected_result = [False, True, True, False, False, False, False, False]
    for page, (current, expected) in enumerate(zip(extracted, expected_result)):
        if expected:
            assert current > 0.75, f'page {page} value: {current}'
        else:
            assert current < 0.05, f'page: {page} value: {current}'
