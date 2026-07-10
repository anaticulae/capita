# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

# pylint:disable=W0611
from tests.fixtures.docu027 import docu027_fontstore
from tests.fixtures.docu027 import docu027_sections_manual
from tests.fixtures.docu027 import docu027_text
from tests.fixtures.paper import paper18

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    (hoverpower.BACHELOR056_PDF, '0:55'),
    (hoverpower.BACHELOR090_PDF, '0:20,75:90'),
    (hoverpower.BACHELOR241_PDF, '60:80'),
    (hoverpower.DISS143_PDF, '120:135'),
    (hoverpower.DISS167_PDF, '10:20'),
    (hoverpower.DISS173_PDF, '0:50'),
    (hoverpower.DISS264_PDF, '0:50,215:234'),
    (hoverpower.DISS406_PDF, '0:50'),
    (hoverpower.MASTER112_PDF, '0:40'),
    (hoverpower.MASTER116_PDF, '0:13,85:117'),
    hoverpower.BACHELOR029A_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR077_PDF,
    hoverpower.BACHELOR111_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.BOOK173_PDF,
    hoverpower.DISS148_PDF,
    hoverpower.DISS170_PDF,
    hoverpower.DISS172_PDF,
    hoverpower.DISS180_PDF,
    hoverpower.DISS205_PDF,
    hoverpower.DISS266_PDF,
    hoverpower.DISS287_PDF,
    hoverpower.DOCU007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU014_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.DOCU035_PDF,
    # hoverpower.HC_DISS128,
    # hoverpower.HC_DISS148,
    # hoverpower.HC_DISS166,
    # hoverpower.HC_DISS171,
    # hoverpower.HC_DISS193,
    hoverpower.HOME018_PDF,
    hoverpower.MASTER031_PDF,
    hoverpower.MASTER049_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER083_PDF,
    hoverpower.MASTER091A_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER110_PDF,
    hoverpower.MASTER148_PDF,
    hoverpower.MASTER155_PDF,
    hoverpower.MASTER193_PDF,
    hoverpower.ORDER107_PDF,
    hoverpower.PAPER018_PDF,
]
WORKER = utilotest.worker_count(4, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        base=hoverpower.REPO,
        files=resources,
        cleanup=True,
        footnote=True,
        groupme='--hefopa',
        headnote=True,
        pagenumber=True,
        sections_ref=True,
        worker=WORKER,
    )
