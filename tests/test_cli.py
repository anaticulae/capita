# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import power
import pytest
import serializeraw
import utila
import utilatest

import sections
import tests


def diss266(result):
    expected = [  # TODO: MAY CHANGE LATER
        (iamraw.sections.Introduction, 0, 4),
        (iamraw.sections.MainPart, 4, 214),
        (iamraw.sections.Appendix, 214, 253),
        (iamraw.sections.MainPart, 253, 266),
    ]
    current = [(type(item), item.start, item.end) for item in result]
    assert current == expected


@pytest.mark.parametrize('source, validate', [
    pytest.param(power.BACHELOR111_PDF, None, id='bachelor111'),
    pytest.param(power.BACHELOR063_PDF, None, id='bachelor63'),
    pytest.param(power.DOCU07_PDF, None, id='howto'),
    pytest.param(power.DOCU09_PDF, None, id='pyporting'),
    pytest.param(power.DOCU27_PDF, None, id='restruct'),
    pytest.param(power.DISS266_PDF, diss266, id='diss266'),
])
@utilatest.skip_longrun
def test_run_sections(source, validate, testdir, monkeypatch):
    source = power.link(source)
    command = f'-i {source}'
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
