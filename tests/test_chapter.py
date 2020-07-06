# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import iamraw.path
import pytest
import serializeraw
import texmex
import utila

import sections.feature.chapter
import tests.resources

RESTRUCT_TEXT = iamraw.path.text(tests.resources.RESTRUCT)
RESTRUCT_TEXT_POSITION = iamraw.path.textposition(tests.resources.RESTRUCT)
RESTRUCT_TOC = iamraw.path.toc(tests.resources.RESTRUCT)


@pytest.mark.parametrize('document, position, toc, expected', [
    pytest.param(
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        RESTRUCT_TOC,
        [6, 8, 10, 12, 18, 20, 22, 24],
        id='restruct',
    ),
    pytest.param(
        iamraw.path.text(tests.resources.MASTER72),
        iamraw.path.textposition(tests.resources.MASTER72),
        iamraw.path.toc(tests.resources.MASTER72),
        [3, 6, 22, 45, 63],
        id='master72pages',
    ),
])
def test_chapter_extract(document, position, toc, expected):
    result = extract_chapter(document, position, toc)

    pages = [item.page for item in result]

    assert pages == expected


@pytest.mark.parametrize('document, position, toc', [
    pytest.param(
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        RESTRUCT_TOC,
        id='restruct',
    ),
])
def test_chapter_dump_and_load_detection(document, position, toc):
    result = extract_chapter(document, position, toc)

    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)

    assert loaded == result


def extract_chapter(document, position, toc):
    # load
    document = serializeraw.load_document(document)
    position = serializeraw.load_textpositions(position)
    tocs = serializeraw.load_toc(toc)

    navigators = texmex.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    result = sections.feature.chapter.extract_chapter(
        navigators,
        tocs,
    )
    return result


def chapter(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    tocs = groupme.path.toc(source)

    dumped = sections.feature.chapter.work(
        text,
        textposition,
        tocpath=tocs,
        pages=pages,
    )
    assert dumped, dumped

    loaded = serializeraw.load_likelihood(dumped)
    return loaded


def test_chapter_work_bachelor63():
    source = tests.resources.BACHELOR63
    extracted = chapter(source)
    # Einleitung
    first_chapter = utila.select_page(extracted, page=8)
    assert first_chapter.content.value >= 0.5, str(extracted)

    # Grundlagen
    second_chapter = utila.select_page(extracted, page=9)
    assert second_chapter.content.value >= 0.5, str(extracted)

    expected = [2, 3, 4, 5, 8, 9, 17, 19, 59]
    pages = [item.page for item in extracted]

    assert pages == expected


def test_chapter_work_master98():
    source = tests.resources.MASTER98
    extracted = chapter(source)

    expected = [2, 6, 26, 42, 67, 85, 88, 96]
    pages = [item.page for item in extracted]

    assert pages == expected
