# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests.validation.bachelor

EXPECTED_FAILURE = {
    power.BACHELOR056_PDF,
    power.BACHELOR111_PDF,
}


def determine_mark(pdf):
    if pdf in EXPECTED_FAILURE:
        return pytest.mark.xfail(reason='expected failure')
    return pytest.mark.huge


SECTIONS = {}
SECTIONS.update(tests.validation.bachelor.BACHELOR)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        key,
        value,
        id=utila.file_name(key),
        marks=determine_mark(key),
    ) for key, value in SECTIONS.items()
])
@utilatest.nightly
def test_run_validation(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    # run extractor
    extracted = tests.sections_from_dir(
        pdf=source,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
    # validate
    content = [item.__class__ for item in extracted]
    sectiontype = [item[0] for item in expected]
    utila.log(f'expected: {sectiontype}')
    utila.log(f'current: {content}')
    assert content == sectiontype, str(content)
    pagestartend = [item[1] for item in expected]
    current = [(item.start, item.end) for item in extracted]
    assert current == pagestartend
