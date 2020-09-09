# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utila
import utilatest

import sections.feature.section
import tests.resources.update
import tests.validation.bachelor
import tests.validation.master

EXPECTED_FAILURE = {
    power.BACHELOR037_PDF,
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
            id=utila.make_relative(key, power.REPOSITORY),
            marks=determine_mark(key),
        ) for key, value in SECTIONS.items()
    ],
)
@utilatest.skip_nightly
def test_run_validation(source, expected, testdir):
    root = testdir.tmpdir
    job = genex.create_job(
        source,
        root,
        config=dict(groupme=True),
        rawmaker=genex.CONFIG,
        oneline=genex.ONELINE,
    )
    utila.run(job)

    extracted = sections.feature.section.extract_sections_frompath(root)

    content = [item.__class__ for item in extracted]
    sectiontype = [item[0] for item in expected]
    utila.log(f'expected: {sectiontype}')
    utila.log(f'current: {content}')
    assert content == sectiontype, str(content)

    pagestartend = [item[1] for item in expected]
    current = [(item.start, item.end) for item in extracted]
    assert current == pagestartend
