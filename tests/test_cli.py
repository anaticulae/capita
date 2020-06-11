# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import pytest
import serializeraw
import utila

import sections.path
import tests
import tests.resources


def bachelor63(items):
    assert len(items) == 3

    introduction = items[0]
    assert isinstance(introduction, iamraw.sections.Introduction)
    assert (introduction.start, introduction.end) == (0, 8)

    mainpart = items[1]
    assert isinstance(mainpart, iamraw.sections.MainPart)
    assert (mainpart.start, mainpart.end) == (8, 59)

    appendix = items[2]
    assert isinstance(appendix, iamraw.sections.Appendix)
    assert (appendix.start, appendix.end) == (59, 62)


# yapf:disable
@pytest.mark.parametrize('command, validate', [
    pytest.param(f'-i {tests.resources.BACHELOR111}', None, id='bachelor111'),
    pytest.param(f'-i {tests.resources.BACHELOR63}', bachelor63, id='bachelor63'),
    pytest.param(f'-i {tests.resources.HOWTO_PYPORTING}', None, id='howto'),
    pytest.param(f'-i {tests.resources.PYPORTING}', None, id='pyporting'),
    pytest.param(f'-i {tests.resources.RESTRUCT}', None, id='restruct'),
])
# yapf:enable
def test_run_sections(command, validate, testdir, monkeypatch):
    """Run help and version and format command to reach basic test coverage"""
    tests.run_sections(command, monkeypatch=monkeypatch)

    loaded = serializeraw.load_sections(sections.path.sections_(testdir.tmpdir))

    if validate:
        validate(loaded)


@pytest.mark.parametrize('command', [
    ['-i', tests.resources.RESTRUCT_PDF, '-o', '.', '--all'],
])
def test_run_sections_failed(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run `sections` with bad input"""
    tests.run_sections_failure(command, monkeypatch=monkeypatch)


@utila.skip_longrun
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
    utila.copy_content(tests.resources.MASTER72, root, pattern=pattern)

    jobs = 5
    cmd = f'-j{jobs} -i {root} -o {root} --pages=0:5 --all'
    tests.run_sections(cmd, monkeypatch=monkeypatch)
