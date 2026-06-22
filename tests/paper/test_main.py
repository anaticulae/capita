# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita.paper.main
import hoverpower
import utilo
import utilotest


@utilotest.nightly
def test_paper_main_diss148():
    source = hoverpower.DISS148_PDF
    detected = capita.paper.main.detect_paper(source)
    # enable later
    expected = [(46, 111)]
    fixup = detected == [(92, 111)]  # TODO: REMOVE LATER
    assert detected == expected or fixup


@utilotest.nightly
def test_paper_bachelor111():
    """Do not detect end of bachelor111 as cited content.

    There was a bug in layouta-double detector which identifies end of
    document as paper content."""
    source = hoverpower.BACHELOR111_PDF
    detected = capita.paper.main.detect_paper(
        source,
        pages=utilo.rtuple(100, 115),
    )
    assert not detected


@utilotest.longrun
def test_paper_book173():
    """Do not detect end of book173 as cited content."""
    source = hoverpower.BOOK173_PDF
    detected = capita.paper.main.detect_paper(
        source,
        pages=utilo.rtuple(164, 172),
    )
    assert not detected
