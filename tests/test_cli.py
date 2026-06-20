# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilo
import utilotest

import tests


@pytest.mark.parametrize('cmd', [
    pytest.param(f'-i {hoverpower.DOCU027_PDF} -o . --all', id='docu27'),
])
def test_run_sections_failed(cmd, td, mp):  #pylint: disable=W0613
    """Run `sections` with bad input"""
    tests.fail(cmd, mp=mp)


@utilotest.nightly
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_run_sections_multicore(td, mp):
    """Regression test to ensure the correct order of the different
    steps in multicore behavior.

    There was a bug in the order of steps. `sections` step was runned to
    early and the required test data were not generated.

    Solved by: upgrading utilo lib.
    """
    source = hoverpower.link(hoverpower.MASTER072_PDF)
    # this step is required, cause the test generator already generates
    # this required items.
    # Copy yaml files which starts with rawmaker or groupme.
    pattern = '(rawmaker|groupme|pdfinfo|sections_ref)*.yaml'
    utilo.copy_content(source, td.tmpdir, pattern=pattern)
    jobs = 5
    cmd = f'-j{jobs} -i {td.tmpdir} -o {td.tmpdir} --pages=0:5 --all'
    tests.run(cmd, mp=mp)
