# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

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
