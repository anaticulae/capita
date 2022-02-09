# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import sections
# pylint:disable=W0611
from tests.fixtures.docu027 import docu027_fontstore
from tests.fixtures.docu027 import docu027_fontstore_fixture
from tests.fixtures.docu027 import docu027_sections_manual
from tests.fixtures.docu027 import docu027_text
from tests.fixtures.paper import paper18

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(sections.ROOT)

PACKAGE = sections.PACKAGE

WORKER = 6

RESOURCES = [
    power.DISS266_PDF,
    power.DISS205_PDF,
    power.MASTER193_PDF,
    power.DISS180_PDF,
    power.BOOK173_PDF,
    power.DISS172_PDF,
    power.DISS170_PDF,
    power.MASTER155_PDF,
    power.DISS148_PDF,
    power.BACHELOR128_PDF,
    power.BACHELOR111_PDF,
    power.MASTER110_PDF,
    power.ORDER107_PDF,
    power.MASTER098_PDF,
    power.MASTER091A_PDF,
    power.MASTER083_PDF,
    power.MASTER075_PDF,
    power.MASTER072_PDF,
    (power.DISS264_PDF, '0:50,215:234'),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER112_PDF, '0:40'),
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.DOCU035_PDF,
    power.MASTER031_PDF,
    power.BACHELOR063_PDF,
    power.MASTER049_PDF,
    (power.MASTER116_PDF, '0:13,85:117'),
    (power.BACHELOR090_PDF, '0:20,75:90'),
    (power.BACHELOR241_PDF, '60:80'),
    power.DOCU027_PDF,
    (power.DISS406_PDF, '0:50'),
    power.PAPER018_PDF,
    power.HOME018_PDF,
    (power.DISS143_PDF, '120:135'),
    (power.DISS167_PDF, '10:20'),
    power.DOCU014_PDF,
    power.DOCU009_PDF,
    power.DOCU007_PDF,
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
        pages=':',
    )
