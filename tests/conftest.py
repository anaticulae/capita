# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import sections
import tests.resources.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = sections.PACKAGE
RESOURCES = tests.resources.update.RESOURCES

WORKER = 6

power.setup(sections.ROOT)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.update.REQURIED_RESOURCES)


def extract(resources):
    # ensure to handle single file generation or common resource subfolder
    # correctly. To determine the output path it is required to determine
    # the parent path of at least two files. If resources provide only a
    # single file the parental determination is not possible. Therefore we
    # have to add the data root of all test files.
    resources.append(power.REPOSITORY)

    genex.extract(
        files=resources,
        destination=power.generated(),
        worker=WORKER,
        groupme=True,
    )
