# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sections.paper.fonts


def test_fonts_bypage(paper18):
    # this test is not very usefull yet. Fonts where not used in the moment.
    parsed = sections.paper.fonts.bypage(paper18)
    assert parsed
