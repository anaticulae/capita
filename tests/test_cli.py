# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import sections
import tests

BACHELOR111 = power.link(power.BACHELOR111_PDF)
BACHELOR063 = power.link(power.BACHELOR063_PDF)


@pytest.mark.parametrize('command, validate', [
    pytest.param(f'-i {BACHELOR111}', None, id='bachelor111'),
    pytest.param(f'-i {BACHELOR063}', None, id='bachelor63'),
    pytest.param(f'-i {power.link(power.DOCU07_PDF)}', None, id='howto'),
    pytest.param(f'-i {power.link(power.DOCU09_PDF)}', None, id='pyporting'),
    pytest.param(f'-i {power.link(power.DOCU27_PDF)}', None, id='restruct'),
])
@utilatest.skip_longrun
def test_run_sections(command, validate, testdir, monkeypatch):
    """Run help and version and format command to reach basic test coverage"""
    tests.run_sections(command, monkeypatch=monkeypatch)

    loaded = serializeraw.load_sections(sections.path.sections_(testdir.tmpdir))

    if validate:
        validate(loaded)


@pytest.mark.parametrize('command', [
    ['-i', power.DOCU27_PDF, '-o', '.', '--all'],
])
def test_run_sections_failed(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run `sections` with bad input"""
    tests.run_sections_failure(command, monkeypatch=monkeypatch)


@utilatest.skip_nightly
def test_run_sections_multicore(testdir, monkeypatch):
    """Regression test to ensure the correct order of the different
    steps in multicore behavior.

    There was a bug in the order of steps. `sections` step was runned to
    early and the required test data were not generated.

    Solved by: upgrading utila lib.
    """
    root = str(testdir)
    # this step is required, cause the test generator already generates
    # this required items.
    # Copy yaml files which starts with rawmaker or groupme.
    pattern = '(rawmaker|groupme)__*.yaml'
    utila.copy_content(power.link(power.MASTER072_PDF), root, pattern=pattern)

    jobs = 5
    cmd = f'-j{jobs} -i {root} -o {root} --pages=0:5 --all'
    tests.run_sections(cmd, monkeypatch=monkeypatch)
