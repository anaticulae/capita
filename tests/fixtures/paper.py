# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest


@pytest.fixture
def paper18():
    utilotest.fixture_requires(hoverpower.PAPER018_PDF)
    source = hoverpower.link(hoverpower.PAPER018_PDF)
    navigator = serializeraw.ptn_frompath(source)
    return navigator
