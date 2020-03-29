# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import sections.feature.section
import tests.resources.update
import tests.validation.bachelor
import tests.validation.master

EXPECTED_FAILURE = {
    tests.resources.BACHELOR37_PDF,
    tests.resources.BACHELOR56_PDF,
    tests.resources.BACHELOR63_PDF,
    tests.resources.BACHELOR111_PDF,
    tests.resources.MASTER72_PDF,
}


def determine_mark(pdf):
    if pdf in EXPECTED_FAILURE:
        return pytest.mark.xfail(reason='expected failure')
    return pytest.mark.huge


SECTIONS = {}
SECTIONS.update(tests.validation.bachelor.BACHELOR)
SECTIONS.update(tests.validation.master.MASTER)


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(
            key,
            value,
            id=utila.make_relative(key, tests.resources.RESOURCES),
            marks=determine_mark(key),
        ) for key, value in SECTIONS.items()
    ],
)
@utila.skip_nightly
def test_run_validation(source, expected, testdir):
    root = testdir.tmpdir
    tests.resources.update.run_package(source, root)
    extracted = sections.feature.section.extract_sections_frompath(root)

    content = [item.__class__ for item in extracted]
    expected = [item[0] for item in expected]
    utila.log('expected:' + str(expected))
    utila.log('current:' + str(content))
    assert content == expected, str(content)
