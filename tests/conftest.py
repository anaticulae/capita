# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest

import sections
import tests.resources.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = sections.PACKAGE

power.setup(sections.ROOT)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.update.REQURIED_RESOURCES)


def extract():
    tests.resources.update.extract_examples()
