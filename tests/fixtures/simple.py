# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import sections.feature.section
import tests.resources


@pytest.fixture
def simple_sections():
    result = sections.feature.section.extract_sections_frompath(
        tests.resources.HOWTO_PYPORTING)
    return result
