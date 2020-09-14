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

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(sections.ROOT)

PACKAGE = sections.PACKAGE

WORKER = 6

RESOURCES = [
    (power.MASTER072_PDF, None),
    (power.MASTER098_PDF, None),
    (power.BACHELOR037_PDF, None),
    (power.DISS264_PDF, '0:50'),
    (power.BACHELOR063_PDF, '0:20,59,60,61'),
    (power.BACHELOR111_PDF, '0:10,90:111'),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER116_PDF, '0:13,85:117'),
    (power.BACHELOR090_PDF, '0:20,75:90'),
    (power.DOCU14_PDF, None),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.DOCU27_PDF, None),
    (power.DOCU35_PDF, None),
    (power.PAPER18_PDF, None),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


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
