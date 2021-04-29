# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
    (power.DISS266_PDF, None),
    (power.DISS170_PDF, None),
    (power.MASTER110_PDF, None),
    (power.MASTER072_PDF, None),
    (power.MASTER098_PDF, None),
    (power.BACHELOR128_PDF, None),
    (power.BACHELOR037_PDF, None),
    (power.DOCU35_PDF, None),
    (power.ORDER109_PDF, None),  # TODO: CHANGE TO 107
    (power.MASTER031_PDF, None),
    (power.MASTER075_PDF, None),
    (power.DISS264_PDF, '0:50,215:234'),
    (power.BACHELOR063_PDF, '0:20,59,60,61'),
    (power.BACHELOR111_PDF, '0:10,90:111'),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER116_PDF, '0:13,85:117'),
    (power.BACHELOR090_PDF, '0:20,75:90'),
    (power.MASTER155_PDF, '0:30'),
    (power.DOCU27_PDF, None),
    (power.PAPER18_PDF, None),
    (power.HOME018_PDF, None),
    (power.DOCU14_PDF, None),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.MASTER112_PDF, '0:40'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        base=power.REPOSITORY,
        destination=power.generated(),
        files=resources,
        groupme=True,
        worker=WORKER,
    )
