# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests.section
import tests.validation.bachelor
import tests.validation.docu
import tests.validation.master

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
SECTIONS.update(tests.validation.docu.DOCU)
SECTIONS.update(tests.validation.master.MASTER)


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(
            key,
            value,
            id=utilatest.simple(key, maxlength=15),
            marks=determine_mark(key),
        ) for key, value in SECTIONS.items()
    ],
)
@utilatest.nightly
def test_run_validation(source, expected):
    utilatest.fixture_requires(source)
    # run extractor
    extracted = tests.section.extract_sections_frompath(source)
    # validate
    content = [item.__class__ for item in extracted]
    sectiontype = [item[0] for item in expected]
    utila.log(f'expected: {sectiontype}')
    utila.log(f'current: {content}')
    assert content == sectiontype, str(content)

    pagestartend = [item[1] for item in expected]
    current = [(item.start, item.end) for item in extracted]
    assert current == pagestartend
