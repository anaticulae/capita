# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import iamraw.path
import iamraw.sections
import pytest
import serializeraw
import utilotest

import sections.creator


@pytest.fixture
def docu027_text() -> iamraw.Document:
    utilotest.fixture_requires(hoverpower.DOCU027_PDF)
    loaded = serializeraw.load_document(hoverpower.link(hoverpower.DOCU027_PDF))
    return loaded


@pytest.fixture
def docu027_fontstore() -> iamraw.FontStore:
    utilotest.fixture_requires(hoverpower.DOCU027_PDF)
    lookup = serializeraw.create_fontstore(
        hoverpower.link(hoverpower.DOCU027_PDF),
        hoverpower.link(hoverpower.DOCU027_PDF),
    )
    return lookup


@pytest.fixture
def docu027_sections_manual() -> iamraw.sections.Sections:
    result = iamraw.sections.Sections()

    def analyse(section, start, end):
        return section(result, start, end, iamraw.sections.PERCENT_100)
        # TODO: reactivate [start, START] later
        # return section(result, [start, START], [end, END], PERCENT_100)

    def add_children(parent, ctor, start, end):
        # new = ctor(parent, [start, START], [end, END], PERCENT_100)
        new = ctor(parent, start, end, iamraw.sections.PERCENT_100)
        return new

    # Page, Start
    # Intro
    intro = analyse(sections.creator.add_introduction, 0, 6)
    add_children(intro, sections.creator.add_title, 0, 0)
    add_children(intro, sections.creator.add_whitepage, 1, 1)
    add_children(intro, sections.creator.add_toc, 2, 2)
    add_children(intro, sections.creator.add_whitepage, 3, 3)
    add_children(intro, sections.creator.add_text, 4, 4)
    add_children(intro, sections.creator.add_whitepage, 5, 5)

    # Content starts here
    content = analyse(sections.creator.add_content, 6, 26)
    sections.creator.add_chapter(content, 6, 7, number=1)
    sections.creator.add_chapter(content, 8, 9, number=2)
    sections.creator.add_chapter(content, 10, 11, number=3)
    sections.creator.add_chapter(content, 12, 17, number=4)
    sections.creator.add_chapter(content, 18, 19, number=5)
    sections.creator.add_chapter(content, 20, 21, number=6)
    sections.creator.add_chapter(content, 22, 23, number=7)
    sections.creator.add_chapter(content, 24, 25, number=8)

    # Second pages with table
    table_second = analyse(sections.creator.add_table, 26, 27)
    add_children(table_second, sections.creator.add_index, 26, 26)

    return result
