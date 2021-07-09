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
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_fontstore_fixture
from tests.fixtures.restruct import restructured_sections_manual
from tests.fixtures.restruct import restructured_text

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(sections.ROOT)

PACKAGE = sections.PACKAGE

WORKER = 6

RESOURCES = [
    (power.DISS266_PDF, None),
    (power.DISS170_PDF, None),
    (power.MASTER110_PDF, None),
    (power.MASTER155_PDF, None),
    (power.BACHELOR128_PDF, None),
    (power.BACHELOR111_PDF, None),
    (power.ORDER107_PDF, None),
    (power.MASTER098_PDF, None),
    (power.MASTER091A_PDF, None),
    (power.MASTER083_PDF, None),
    (power.MASTER075_PDF, None),
    (power.MASTER072_PDF, None),
    (power.DISS264_PDF, '0:50,215:234'),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER112_PDF, '0:40'),
    (power.BACHELOR037_PDF, None),
    (power.BACHELOR051_PDF, None),
    (power.DOCU35_PDF, None),
    (power.MASTER031_PDF, None),
    (power.BACHELOR063_PDF, '0:20,59,60,61'),
    (power.MASTER116_PDF, '0:13,85:117'),
    (power.BACHELOR090_PDF, '0:20,75:90'),
    (power.BACHELOR241_PDF, '60:80'),
    (power.DOCU27_PDF, None),
    (power.PAPER18_PDF, None),
    (power.HOME018_PDF, None),
    (power.DOCU14_PDF, None),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        base=power.REPOSITORY,
        destination=power.generated(),
        files=resources,
        groupme='--pagenumbers --footer --toc',
        worker=WORKER,
    )
