# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.sections
import power
import pytest
import serializeraw
import utila
import utilatest

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

    check_sections(result, expected)

    # Title and Table of MultipleSection
    expected_chapter = HOWTO_PYPORTING_CHAPTER_PAGE_COUNT
    assert len(result[0].content) == expected_chapter
    # TODO: Test order of multiple items


def check_sections(result, expected):
    assert len(result) == len(expected)
    for current, wanted in zip(result, expected):
        current = current.__class__.__name__
        wanted = wanted.__name__
        assert current == wanted, f'{current} != {wanted}'


def test_sections_simple():
    """Check dumped result of section work method"""
    simple_sections = sections.feature.section.extract_sections_frompath(
        power.link(power.DOCU07_PDF))
    assert len(simple_sections) == 2, len(simple_sections)
    dumped = serializeraw.dump_sections(simple_sections)
    assert len(dumped) > 100, dumped
    loaded = serializeraw.load_sections(dumped)
    assert loaded == simple_sections, loaded


@utilatest.skip_longrun
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
    mainpart = result[1]
    assert isinstance(mainpart, iamraw.sections.MainPart), type(mainpart)
    assert len(mainpart) == 62  # content pages

    chapternumbers = [
        item.start
        for item in utila.select_type(mainpart.content, iamraw.sections.Chapter)
    ]
    expected = [3, 6, 22, 45, 63]
    assert chapternumbers == expected


@utilatest.longrun
def test_sections_bachelor90():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.BACHELOR090_PDF))

    expected = [
        iamraw.sections.Unknown,
        iamraw.sections.Introduction,
        iamraw.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)


@utilatest.skip_longrun
def test_sections_master116():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.MASTER116_PDF))

    expected = [
        iamraw.sections.Introduction,
        iamraw.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)

    intro, mainpart, appendix = result

    assert (intro.start, intro.end) == (0, 8)
    assert (mainpart.start, mainpart.end) == (8, 88)
    assert (appendix.start, appendix.end) == (88, 116)


def test_sections_docu35():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.DOCU35_PDF))

    expected = [
        iamraw.sections.Introduction,
        iamraw.MainPart,
        # TODO: ADD APPENDIX
    ]
    check_sections(result, expected)

    intro, mainpart = result

    assert isinstance(intro[0], iamraw.sections.TitlePage)
    # TODO: ADD BLANK PAGE CHECK
    # assert isinstance(intro[1], iamraw.sections.WhitePage)

    assert (intro.start, intro.end) == (0, 6)
    assert (mainpart.start, mainpart.end) == (6, 35)


@utilatest.skip_longrun
def test_sections_diss264():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.DISS264_PDF))

    expected = [
        iamraw.sections.Introduction,
        iamraw.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)


@utilatest.skip_longrun
def test_sections_master31():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.MASTER031_PDF))

    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)


def test_sections_docu27():
    """Regression test to ensure that no bib is detected on first page.
    Before fixing, there was a divided title/bib page."""
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.DOCU27_PDF))

    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Table,  # TODO: REPLACE WITH APPENDIX?
    ]
    check_sections(result, expected)


@utilatest.longrun
def test_sections_master112():
    """Add test to ensure, that toc is not parsed as bib."""
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.MASTER112_PDF))

    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
    ]
    check_sections(result, expected)

    # page 5
    expected_toc = result[0].content[5]
    assert isinstance(expected_toc, iamraw.sections.TableOfContent)


@pytest.mark.xfail(reason='toc detector changed?')
def test_sections_master075_appendix():
    result = sections.feature.section.extract_sections_frompath(
        power.link(power.MASTER075_PDF),
        pages=(70, 71, 72, 73, 74),
    )
    result = result[0]
    assert isinstance(result, iamraw.sections.Appendix)

    appendix = result.content
    # page 71
    assert isinstance(appendix[1], iamraw.sections.FigureTable)

    # expected
    expected = [
        iamraw.sections.Bibliography,
        iamraw.sections.FigureTable,
        # [  # TODO: SUPPORT MULTIPLE PAGE
        #     iamraw.sections.FigureTable,
        #     iamraw.sections.TableTable,
        # ],
        iamraw.sections.TableTable,
        iamraw.sections.WhitePage,
        iamraw.sections.LegalInformation,
    ]

    for page, valid in zip(appendix, expected):
        assert isinstance(page, valid)
