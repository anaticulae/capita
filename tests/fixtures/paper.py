# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest


@pytest.fixture
def paper18():
    utilatest.fixture_requires(power.PAPER18_PDF)
    source = power.link(power.PAPER18_PDF)
    navigator = serializeraw.create_pagetextnavigators_frompath(source)
    return navigator
