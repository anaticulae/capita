# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

# TODO: MOVE TESTS FROM test_cli.py

# TODO: DOCU027_PDF:iamraw.sections.Table: REPLACE WITH APPENDIX?
SECTIONS_X = [
    (power.DOCU007_PDF, (
        iamraw.sections.Unknown,
        iamraw.sections.MainPart,
    )),
    (power.DOCU009_PDF, (
        iamraw.sections.Unknown,
        iamraw.sections.MainPart,
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
    )),
    (power.DOCU027_PDF, (
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Table,
    )),
    (power.BACHELOR037_PDF, (
        (iamraw.sections.Introduction, 0, 6),
        (iamraw.sections.MainPart, 6, 33),
        (iamraw.sections.Appendix, 33, 37),
    )),
    (power.BACHELOR063_PDF, (
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    )),
    (power.BACHELOR090_PDF, (
        (iamraw.sections.Unknown, 0, 1),
        (iamraw.sections.Introduction, 1, 12),
        (iamraw.MainPart, 12, 76),
        (iamraw.sections.Appendix, 76, 90),
    )),
    (power.BACHELOR111_PDF, (
        (iamraw.sections.Introduction, 0, 5),
        (iamraw.sections.MainPart, 5, 83),
        (iamraw.sections.Appendix, 83, 111),
    )),
    (power.BACHELOR128_PDF, (
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    )),
    (power.MASTER031_PDF, (
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    )),
    (power.MASTER083_PDF, (
        (iamraw.sections.Introduction, 0, 4),
        (iamraw.sections.MainPart, 4, 75),
        (iamraw.sections.Appendix, 75, 83),
    )),
    (power.MASTER116_PDF, (
        (iamraw.sections.Introduction, 0, 8),
        (iamraw.MainPart, 8, 88),
        (iamraw.sections.Appendix, 88, 116),
    )),
    (power.DISS170_PDF, (
        (iamraw.sections.Introduction, 0, 6),
        (iamraw.sections.MainPart, 6, 141),
        (iamraw.sections.Appendix, 141, 170),
    )),
    (power.DISS264_PDF, (
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    )),
    (power.DISS266_PDF, (
        (iamraw.sections.Introduction, 0, 9),
        (iamraw.sections.MainPart, 9, 214),
        (iamraw.sections.Appendix, 214, 266),
    )),
]
SECTIONS_X = [
    pytest.param(
        source,
        pages,
        id=utila.file_name(source),
    ) for source, pages in SECTIONS_X
]


@utilatest.nightly
@pytest.mark.parametrize('source, expected', SECTIONS_X)
def test_sections_x(source, expected, testdir, monkeypatch):
    """\
    DOCU:027 Regression test to ensure that no bib is detected on first
             page. Before fixing, there was a divided title/bib page.
    """
    utilatest.fixture_requires(source)
    result = tests.sections_from_dir(
        source,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
    pages = isinstance(expected[0], tuple)
    expected_sections = [item[0] for item in expected] if pages else expected
    check_sections(result, expected_sections)
    if not pages:
        # no expected pages given
        return
    # pages
    expected_pages = [(item[1], item[2]) for item in expected]
    current_pages = [(item.start, item.end) for item in result]
    assert current_pages == expected_pages


def test_dump_and_load_sections(docu027_sections_manual):
    data = docu027_sections_manual
    dumped = serializeraw.dump_sections(data)
    assert dumped
    loaded = serializeraw.load_sections(dumped)
    assert loaded
    assert loaded == data


def test_validate_docu027(docu027_sections_manual):
    validated = sections.creator.validate(docu027_sections_manual)
    assert validated


@pytest.mark.xfail(reason='chapter detector is too optimistic')
@utilatest.nightly
@utilatest.requires(power.DOCU027_PDF)
def test_extract_sections_docu027(
    testdir,
    monkeypatch,
    docu027_sections_manual,
):
    root = testdir.tmpdir
    source = power.link(power.DOCU027_PDF)
    tests.run_sections(f'-i {source}', monkeypatch=monkeypatch)

    result = sections.feature.section.load_section_likelihood_frompath(root)
    assert result
    for index, (actual,
                expected) in enumerate(zip(
                    result,
                    docu027_sections_manual,
                )):
        # Compare only the first level
        assert actual.start == expected.start, 'on level: %d' % index
        assert actual.end == expected.end, 'on level: %d' % index

    # TODO: activate later, do not want to make this test so explicit
    # assert result == docu027_sections


def test_chapters(docu027_sections_manual):
    result = sections.feature.section.chapters(docu027_sections_manual)
    # start is lower or equal than end page size
    # start = item[0]
    # end   = item[1]
    ascending_page_order = all(item[0] <= item[1] for item in result)
    assert ascending_page_order, str([result])
    assert len(result) == 8, str(result)


HOWTO_PYPORTING_CHAPTER_PAGE_COUNT = 2


@pytest.mark.xfail(reason='require multiple page toc detector')
@utilatest.nightly
@utilatest.requires(power.DOCU007_PDF)
def test_extract_sections_simple(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DOCU007_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
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
    utila.log('current')
    for item in result:
        utila.log(item)
    utila.log()
    utila.log('expected')
    for item in expected:
        utila.log(item)
    assert len(result) == len(expected)
    for current, wanted in zip(result, expected):
        current = current.__class__.__name__
        wanted = wanted.__name__
        assert current == wanted, f'{current} != {wanted}'


@utilatest.nightly
@utilatest.requires(power.DOCU007_PDF)
def test_sections_simple(testdir, monkeypatch):
    """Check dumped result of section work method"""
    simple_sections = tests.sections_from_dir(
        power.DOCU007_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
    assert len(simple_sections) == 2, len(simple_sections)
    dumped = serializeraw.dump_sections(simple_sections)
    assert len(dumped) > 100, dumped
    loaded = serializeraw.load_sections(dumped)
    assert loaded == simple_sections, loaded


@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_sections_master72(testdir, monkeypatch):
    """Ensure that BUILDER in section is sorted correctly. There is a
    problem if we sort TOC and Title alphabetically. To avoid this
    problem this test ensure that sorting due the developer is done
    correctly."""
    result = tests.sections_from_dir(
        power.MASTER072_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
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


@pytest.mark.xfail(reason='too optimistic parser')
@utilatest.nightly
@utilatest.requires(power.DOCU035_PDF)
def test_sections_docu35(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DOCU035_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
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


@utilatest.nightly
@utilatest.requires(power.MASTER112_PDF)
def test_sections_master112(testdir, monkeypatch):
    """Add test to ensure, that toc is not parsed as bib."""
    result = tests.sections_from_dir(
        power.MASTER112_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
    ]
    check_sections(result, expected)
    # page 5
    expected_toc = result[0].content[5]
    assert isinstance(expected_toc, iamraw.sections.TableOfContent)


@utilatest.nightly
@utilatest.requires(power.MASTER075_PDF)
def test_sections_master075_appendix(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.MASTER075_PDF,
        pages='70,71,72,73,74',
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
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


@utilatest.nightly
@utilatest.requires(power.MASTER091A_PDF)
def test_sections_master91a(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.MASTER091A_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    intro, mainpart, appendix = result
    assert (intro.start, intro.end) == (0, 13)
    assert (mainpart.start, mainpart.end) == (13, 74)
    assert (appendix.start, appendix.end) == (74, 91)


@utilatest.nightly
@utilatest.requires(power.DISS148_PDF)
def test_sections_diss148(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DISS148_PDF,
        path=testdir.tmpdir,
        monkeypatch=monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.CitePart,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    intro, mainpart, citepart, secondpart, appendix = result
    assert (intro.start, intro.end) == (0, 18)
    assert (mainpart.start, mainpart.end) == (18, 46)
    assert (citepart.start, citepart.end) == (46, 116)
    assert (secondpart.start, secondpart.end) == (116, 137)
    assert (appendix.start, appendix.end) == (137, 148)


@utilatest.nightly
@utilatest.requires(power.DISS180_PDF)
def test_sections_diss180(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DISS180_PDF,
        testdir,
        monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    intro, mainpart, appendix = result
    assert (intro.start, intro.end) == (0, 18)
    assert (mainpart.start, mainpart.end) == (18, 169)
    assert (appendix.start, appendix.end) == (169, 180)


@utilatest.nightly
@utilatest.requires(power.DISS205_PDF)
def test_sections_diss205(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DISS205_PDF,
        testdir,
        monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    intro, mainpart, appendix = result
    assert (intro.start, intro.end) == (0, 16)
    assert (mainpart.start, mainpart.end) == (16, 176)
    assert (appendix.start, appendix.end) == (176, 205)


@utilatest.nightly
@utilatest.requires(power.DISS172_PDF)
def test_sections_diss172(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DISS172_PDF,
        testdir,
        monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    intro, mainpart, appendix = result
    assert (intro.start, intro.end) == (0, 16)
    assert (mainpart.start, mainpart.end) == (16, 150)
    assert (appendix.start, appendix.end) == (150, 172)


@utilatest.nightly
@utilatest.requires(power.DISS406_PDF)
def test_sections_diss406pages50(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.DISS406_PDF,
        testdir,
        monkeypatch,
        pages='0:50',
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        # iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    # intro, mainpart, appendix = result
    intro, mainpart = result
    assert (intro.start, intro.end) == (0, 22)
    assert (mainpart.start, mainpart.end) == (22, 50)
    # assert (appendix.start, appendix.end) == (150, 172)


@utilatest.nightly
@utilatest.requires(power.MASTER193_PDF)
def test_sections_master193(testdir, monkeypatch):
    result = tests.sections_from_dir(
        power.MASTER193_PDF,
        testdir,
        monkeypatch,
    )
    expected = [
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
        iamraw.sections.Appendix,
    ]
    check_sections(result, expected)
    intro, mainpart, appendix = result
    assert (intro.start, intro.end) == (0, 6)
    assert (mainpart.start, mainpart.end) == (6, 188)
    assert (appendix.start, appendix.end) == (188, 193)


@utilatest.nightly
def test_sections_book173(testdir, monkeypatch):
    """Do not detect MainPart before Toc."""
    result = tests.sections_from_dir(
        power.BOOK173_PDF,
        testdir,
        monkeypatch,
        pages='0:30',
    )
    expected = [
        iamraw.sections.Unknown,
        iamraw.sections.Introduction,
        iamraw.sections.MainPart,
    ]
    check_sections(result, expected)
    unknown, intro, mainpart = result
    assert (unknown.start, unknown.end) == (0, 1)
    assert (intro.start, intro.end) == (1, 13)
    assert (mainpart.start, mainpart.end) == (13, 30)
