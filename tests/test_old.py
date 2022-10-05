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


@utilatest.nightly
@utilatest.requires(power.DOCU007_PDF)
def test_sections_simple(td, mp):
    """Check dumped result of section work method"""
    simple_sections = tests.sections_from_dir(
        power.DOCU007_PDF,
        path=td.tmpdir,
        mp=mp,
    )
    assert len(simple_sections) == 2, len(simple_sections)
    dumped = serializeraw.dump_sections(simple_sections)
    assert len(dumped) > 100, dumped
    loaded = serializeraw.load_sections(dumped)
    assert loaded == simple_sections, loaded


@utilatest.nightly
@utilatest.requires(power.MASTER072_PDF)
def test_sections_master72(td, mp):
    """Ensure that BUILDER in section is sorted correctly.

    There is a problem if we sort TOC and Title alphabetically. To avoid
    this problem this test ensure that sorting due the developer is done
    correctly.
    """
    result = tests.sections_from_dir(
        power.MASTER072_PDF,
        path=td.tmpdir,
        mp=mp,
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


@pytest.mark.xfail(reason='software integration')
@utilatest.nightly
@utilatest.requires(power.MASTER075_PDF)
def test_sections_master075_appendix(td, mp):
    result = tests.sections_from_dir(
        power.MASTER075_PDF,
        pages='70,71,72,73,74',
        path=td.tmpdir,
        mp=mp,
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
