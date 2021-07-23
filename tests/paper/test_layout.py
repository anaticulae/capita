# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import sections.paper.layout


@utilatest.longrun
def test_layout():
    percent = sections.paper.layout.percentage(power.PAPER14_PDF)
    expected = (0.61, 1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.4, 0.5,
                1.0, 1.0)
    assert utila.nears(percent, expected, 0.10)


def test_layout_page2_page10():
    percent = sections.paper.layout.percentage(power.PAPER14_PDF, pages=2)
    assert utila.near(percent[0], 0.25, diff=0.15)  # VALIDATED
    percent = sections.paper.layout.percentage(power.PAPER14_PDF, pages=10)
    assert utila.near(percent[0], 0.55, diff=0.15)  # VALIDATED


@pytest.mark.parametrize('source', [
    pytest.param(power.PAPER18_PDF, id='paper18'),
    pytest.param(power.PAPER23_PDF, id='paper23'),
    pytest.param(power.PAPER42_PDF, id='paper42'),
])
@utilatest.nightly
def test_layout_no_double_column(source):
    percent = sections.paper.layout.percentage(source)
    counted = len([item for item in percent if item is not None and item > 0.5])
    assert counted < 5, counted


@pytest.mark.parametrize('source', [
    pytest.param(power.PAPER06_PDF, id='paper6'),
    pytest.param(power.PAPER06B_PDF, id='paper6b'),
    pytest.param(power.PAPER06MATH_PDF, id='paper6math'),
    pytest.param(power.PAPER09_PDF, id='paper09'),
    pytest.param(power.PAPER10_PDF, id='paper10'),
])
@utilatest.longrun
def test_layout_double_column(source):
    percent = sections.paper.layout.percentage(source)
    counted = len([item for item in percent if item is not None and item > 0.6])
    rate = counted / len(percent)
    assert rate >= 0.8, rate
