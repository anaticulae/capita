# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila

import sections.creator
import sections.feature.section
import tests
import tests.resources
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_sections_manual


def test_dump_and_load_sections(restructured_sections_manual):  #pylint:disable=W0621
    data = restructured_sections_manual

    dumped = serializeraw.dump_sections(data)
    assert dumped

    loaded = serializeraw.load_sections(dumped)
    assert loaded

    assert loaded == data


def test_validate_restructured(restructured_sections_manual):  #pylint:disable=W0621
    validated = sections.creator.validate(restructured_sections_manual)
    assert validated


#pylint:disable=W0621
def test_extract_sections_restructured(
        testdir,
        monkeypatch,
        restructured_sections_manual,
):
    root = testdir.tmpdir
    source = power.link(power.DOCU27_PDF)
    tests.run_sections(f'-i {source}', monkeypatch=monkeypatch)

    result = sections.feature.section.load_section_likelihood_frompath(root)
    assert result
    for index, (actual, expected) in enumerate(
            zip(result, restructured_sections_manual)):
        # Compare only the first level
        assert actual.start == expected.start, 'on level: %d' % index
        assert actual.end == expected.end, 'on level: %d' % index

    # TODO: activate later, do not want to make this test so explicit
    # assert result == restructured_sections


def test_chapters(restructured_sections_manual):
    result = sections.feature.section.chapters(restructured_sections_manual)

    # start is lower or equal than end page size
    # start = item[0]
    # end   = item[1]
    ascending_page_order = all([item[0] <= item[1] for item in result])

    assert ascending_page_order, str([result])
    assert len(result) == 8, str(result)


HOWTO_PYPORTING_CHAPTER_PAGE_COUNT = 2


@pytest.mark.xfail(reason='require multiple page toc detector')
def test_extract_sections_simple():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.DOCU07_PDF))

    expected = [
        iamraw.MultipleSection,
        iamraw.MainPart,
    ]

    assert len(result) == len(expected), 'wrong area split'
    for current, wanted in zip(result, expected):
        current = current.__class__.__name__
        wanted = wanted.__name__
        assert current == wanted, f'{current} != {wanted}'

    # Title and Table of MultipleSection
    expected_chapter = HOWTO_PYPORTING_CHAPTER_PAGE_COUNT
    assert len(result[0].content) == expected_chapter
    # TODO: Test order of multiple items


def test_sections_simple():
    """Check dumped result of section work method"""
    simple_sections = sections.feature.section.extract_sections_frompath(
        power.link(power.DOCU07_PDF))
    assert len(simple_sections) == 2, len(simple_sections)
    dumped = serializeraw.dump_sections(simple_sections)
    assert len(dumped) > 100, dumped
    loaded = serializeraw.load_sections(dumped)
    assert loaded == simple_sections, loaded


def test_sections_master72():
    """Ensure that BUILDER in section is sorted correctly. There is a
    problem if we sort TOC and Title alphabetically. To avoid this
    problem this test ensure that sorting due the developer is done
    correctly."""
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.MASTER072_PDF))
    # page 0 is title page
    assert isinstance(result[0], iamraw.sections.Introduction), type(result[0])
    # page 1 and 2 is introduction
    assert isinstance(result[1], iamraw.sections.MainPart), type(result[1])
    assert len(result[1]) == 62  # content pages


def test_sections_bachelor90_pages0_15():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.BACHELOR090_PDF),
        pages=utila.ranged_tuple(0, 16),
    )

    expected = [
        iamraw.sections.Unknown,
        iamraw.sections.Introduction,
        iamraw.MainPart,
    ]
    assert len(result) == len(expected)

    for current, wanted in zip(result, expected):
        current = current.__class__.__name__
        wanted = wanted.__name__
        assert current == wanted, f'{current} != {wanted}'
