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
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

# pylint:disable=W0611
from tests.fixtures.docu027 import docu027_fontstore
from tests.fixtures.docu027 import docu027_sections_manual
from tests.fixtures.docu027 import docu027_text
from tests.fixtures.paper import paper18

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(__file__)

RESOURCES = [
    (power.BACHELOR056_PDF, '0:55'),
    (power.BACHELOR090_PDF, '0:20,75:90'),
    (power.BACHELOR241_PDF, '60:80'),
    (power.DISS143_PDF, '120:135'),
    (power.DISS167_PDF, '10:20'),
    (power.DISS173_PDF, '0:50'),
    (power.DISS264_PDF, '0:50,215:234'),
    (power.DISS406_PDF, '0:50'),
    (power.MASTER112_PDF, '0:40'),
    (power.MASTER116_PDF, '0:13,85:117'),
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR076_PDF,
    power.BACHELOR077_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR128_PDF,
    power.BOOK173_PDF,
    power.DISS148_PDF,
    power.DISS170_PDF,
    power.DISS172_PDF,
    power.DISS180_PDF,
    power.DISS205_PDF,
    power.DISS266_PDF,
    power.DISS287_PDF,
    power.DOCU007_PDF,
    power.DOCU009_PDF,
    power.DOCU014_PDF,
    power.DOCU027_PDF,
    power.DOCU035_PDF,
    power.HC_DISS128,
    power.HC_DISS148,
    power.HC_DISS166,
    power.HC_DISS171,
    power.HC_DISS193,
    power.HOME018_PDF,
    power.MASTER031_PDF,
    power.MASTER049_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER083_PDF,
    power.MASTER091A_PDF,
    power.MASTER098_PDF,
    power.MASTER110_PDF,
    power.MASTER148_PDF,
    power.MASTER155_PDF,
    power.MASTER193_PDF,
    power.ORDER107_PDF,
    power.PAPER018_PDF,
]
WORKER = utilatest.worker_count(4, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        base=power.REPOSITORY,
        files=resources,
        cleanup=True,
        footnote=True,
        groupme='--hefopa',
        headnote=True,
        pagenumber=True,
        worker=WORKER,
    )
