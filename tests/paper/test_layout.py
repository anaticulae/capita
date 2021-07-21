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

import sections.paper.layout


def test_layout():
    percent = sections.paper.layout.percentage(power.PAPER14_PDF)
    expected = (0.61, 1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.55, 0.93,
                1.0, 1.0)
    assert percent == expected


def test_layout_page2_page10():
    percent = sections.paper.layout.percentage(power.PAPER14_PDF, pages=2)
    assert percent[0] == 0.25  # VALIDATED
    percent = sections.paper.layout.percentage(power.PAPER14_PDF, pages=10)
    assert percent[0] == 0.55  # VALIDATED


@pytest.mark.parametrize('source', [
    pytest.param(power.PAPER18_PDF, id='paper18'),
    pytest.param(power.PAPER23_PDF, id='paper23'),
    pytest.param(power.PAPER42_PDF, id='paper42'),
])
def test_layout_no_double_column(source):
    percent = sections.paper.layout.percentage(source)
    counted = len([item for item in percent if item is not None and item > 0.5])
    assert counted < 5, counted
