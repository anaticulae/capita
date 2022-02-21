# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import sections.paper.main


@utilatest.nightly
def test_paper_main_diss148():
    source = power.DISS148_PDF
    detected = sections.paper.main.detect_paper(source)
    expected = [(46, 111)]
    assert detected == expected


@utilatest.longrun
def test_paper_bachelor111():
    """Do not detect end of bachelor111 as cited content.

    There was a bug in layout-double detector which identifies end of
    document as paper content."""
    source = power.BACHELOR111_PDF
    detected = sections.paper.main.detect_paper(
        source,
        pages=utila.rtuple(100, 115),
    )
    assert not detected


@utilatest.longrun
def test_paper_book173():
    """Do not detect end of book173 as cited content."""
    source = power.BOOK173_PDF
    detected = sections.paper.main.detect_paper(
        source,
        pages=utila.rtuple(164, 172),
    )
    assert not detected
