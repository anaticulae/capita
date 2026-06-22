# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import capita.paper.fonts


@utilotest.longrun
def test_fonts_bypage(paper18):
    # this test is not very usefull yet. Fonts where not used in the moment.
    parsed = capita.paper.fonts.bypage(paper18)
    assert parsed
