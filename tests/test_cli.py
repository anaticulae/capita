# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


@pytest.mark.parametrize('cmd', [
    pytest.param(f'-i {power.DOCU027_PDF} -o . --all', id='docu27'),
])
def test_run_sections_failed(cmd, td, mp):  #pylint: disable=W0613
    """Run `sections` with bad input"""
    tests.run_sections_failure(cmd, mp=mp)


@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_run_sections_multicore(td, mp):
    """Regression test to ensure the correct order of the different
    steps in multicore behavior.

    There was a bug in the order of steps. `sections` step was runned to
    early and the required test data were not generated.

    Solved by: upgrading utila lib.
    """
    source = power.link(power.MASTER072_PDF)
    # this step is required, cause the test generator already generates
    # this required items.
    # Copy yaml files which starts with rawmaker or groupme.
    pattern = '(rawmaker|groupme|pdfinfo)*.yaml'
    utila.copy_content(source, td.tmpdir, pattern=pattern)
    jobs = 5
    cmd = f'-j{jobs} -i {td.tmpdir} -o {td.tmpdir} --pages=0:5 --all'
    tests.run_sections(cmd, mp=mp)
