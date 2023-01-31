# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest


@pytest.fixture
def paper18():
    utilatest.fixture_requires(power.PAPER018_PDF)
    source = power.link(power.PAPER018_PDF)
    navigator = serializeraw.ptn_frompath(source)
    return navigator
