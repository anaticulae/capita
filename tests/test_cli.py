# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def validate(current, expected):
    current = [(type(item), item.start, item.end) for item in current]
    assert current == expected


def diss266(result):
    expected = [
        (iamraw.sections.Introduction, 0, 9),
        (iamraw.sections.MainPart, 9, 214),
        (iamraw.sections.Appendix, 214, 266),
    ]
    validate(result, expected)


def bachelor37(result):
    expected = [
        (iamraw.sections.Introduction, 0, 6),
        (iamraw.sections.MainPart, 6, 33),
        (iamraw.sections.Appendix, 33, 37),
    ]
    validate(result, expected)


def diss170(result):
    expected = [
        (iamraw.sections.Introduction, 0, 6),
        (iamraw.sections.MainPart, 6, 141),
        (iamraw.sections.Appendix, 141, 170),
    ]
    validate(result, expected)


def master83(result):
    expected = [
        (iamraw.sections.Introduction, 0, 4),
        (iamraw.sections.MainPart, 4, 75),
        (iamraw.sections.Appendix, 75, 83),
    ]
    validate(result, expected)


def bachelor111(result):
    expected = [
        (iamraw.sections.Introduction, 0, 5),
        (iamraw.sections.MainPart, 5, 83),
        (iamraw.sections.Appendix, 83, 111),
    ]
    validate(result, expected)


@pytest.mark.parametrize('pdf, expected', [
    pytest.param(power.BACHELOR037_PDF, bachelor37, id='bachelor37'),
    pytest.param(power.BACHELOR063_PDF, None, id='bachelor63'),
    pytest.param(power.BACHELOR111_PDF, bachelor111, id='bachelor111'),
    pytest.param(power.DISS266_PDF, diss266, id='diss266'),
    pytest.param(power.DOCU007_PDF, None, id='howto'),
    pytest.param(power.DOCU009_PDF, None, id='pyporting'),
    pytest.param(power.DOCU027_PDF, None, id='restruct'),
    pytest.param(power.DISS170_PDF, diss170, id='diss170'),
    pytest.param(power.MASTER083_PDF, master83, id='master83'),
])
@utilatest.nightly
def test_run_sections(pdf, expected, testdir, monkeypatch):
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    command = f'-i {source} --pdf={pdf}'
    # run sections
    tests.run_sections(command, monkeypatch=monkeypatch)
    # validate result
    loaded = serializeraw.load_sections(sections.path.sections_(testdir.tmpdir))
    if not expected:
        return
    expected(loaded)


@pytest.mark.parametrize('command', [
    pytest.param(f'-i {power.DOCU027_PDF} -o . --all', id='docu27'),
])
def test_run_sections_failed(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run `sections` with bad input"""
    tests.run_sections_failure(command, monkeypatch=monkeypatch)


@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_run_sections_multicore(testdir, monkeypatch):
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
    pattern = '(rawmaker|groupme)__*.yaml'
    utila.copy_content(source, testdir.tmpdir, pattern=pattern)
    jobs = 5
    cmd = f'-j{jobs} -i {testdir.tmpdir} -o {testdir.tmpdir} --pages=0:5 --all'
    tests.run_sections(cmd, monkeypatch=monkeypatch)
