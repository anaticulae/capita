# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw.path
import pytest
import serializeraw
import utilo
import utilotest

import capita.chapter.run
import capita.feature.chapter


# TODO: BACHELOR37: ADD HEADLINES IN THE MIDDLE OF THE PAGE LATER
# TODO: DISS266 - IMPROVE LATER
# TODO: REMOVE MASTER91A PAGE 66 later
# BACHELOR51: [3, 4, 20, 28, 35, 40, 42],
# yapf:disable
@pytest.mark.parametrize('source, expected', [
    pytest.param(
        hoverpower.DOCU027_PDF,
        [6, 8, 10, 12, 18, 20, 22, 24],
        id='docu027',
        marks=pytest.mark.xfail(reason='parser is too optimistic'),
    ),
    pytest.param(
        hoverpower.MASTER072_PDF,
        [3, 6, 22, 45, 63],
        id='master72pages',
    ),
    pytest.param(
        hoverpower.MASTER091A_PDF,
        [13, 16, 18, 33, 37, 47, 58, 66, 72, 82],
        id='master91a',
        marks=pytest.mark.xfail(reason='incomplete integration'),
    ),
    pytest.param(
        hoverpower.DISS266_PDF,
        [9, 23, 30, 81, 103, 197, 203],
        # [4, 5, 9, 23, 81, 103, 197, 203, 205],
        id='diss266',
        marks=pytest.mark.xfail(reason='incomplete integration'),
    ),
    pytest.param(
        hoverpower.BACHELOR051_PDF,
        [3, 4, 28, 35, 42],
        id='bachelor51',
    ),
    pytest.param(
        hoverpower.BACHELOR037_PDF,
        # [6, 15, 27],
        [6, 15],
        id='bachelor37',
    ),
    pytest.param(
        hoverpower.BACHELOR111_PDF,
        [5, 8, 31, 40, 52, 66, 80],
        id='bachelor111',
    ),
    pytest.param(
        hoverpower.DISS172_PDF,
        [16, 24, 43, 54, 75, 89, 112, 132, 148, 150],
        # [16, 89, 148, 150],
        id='diss172',
        marks=pytest.mark.xfail(reason='incomplete integration'),
    ),
    pytest.param(
        hoverpower.DISS406_PDF,
        # [22, 25, 40],
        # too optimistic, but this is not a problem
        [22, 26, 40, 48, 49],
        id='diss406',
    ),
])
# yapf:enable
@utilotest.nightly
def test_chapter_extract(source, expected):
    source = hoverpower.link(source)
    # run
    result = extract_chapter(source)
    # verify result
    pages = [item.page for item in result]
    assert pages == expected


@utilotest.longrun
def test_chapter_dump_and_load_detection():
    source = hoverpower.link(hoverpower.DOCU027_PDF)
    result = extract_chapter(source)
    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)
    assert loaded == result


def extract_chapter(source):
    utilotest.fixture_requires(source)
    # load
    navigators = serializeraw.ptcn_frompath(source)
    outlines = serializeraw.load_toc(iamraw.path.outlines(source))
    # run
    result = capita.chapter.run.extract_chapter(
        navigators,
        outlines,
    )
    return result


def chapter(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    utilotest.fixture_requires(source)
    dumped = capita.feature.chapter.work(
        document=iamraw.path.text(source, prefix='oneline'),  # use default path
        position=iamraw.path.textposition(source, prefix='oneline'),
        sizeandborder=source,
        footerheader=source,
        outlines=iamraw.path.outlines(source),
        pages=pages,
    )
    assert dumped, dumped
    loaded = serializeraw.load_likelihood(dumped)
    return loaded


@pytest.mark.xfail(reason='incomplete integration')
@utilotest.longrun
def test_chapter_work_bachelor63():
    source = hoverpower.link(hoverpower.BACHELOR063_PDF)
    extracted = chapter(source)
    # Einleitung
    first_chapter = utilo.select_page(extracted, page=8)
    assert first_chapter.content.value >= 0.5, str(extracted)
    # Grundlagen
    second_chapter = utilo.select_page(extracted, page=9)
    assert second_chapter.content.value >= 0.5, str(extracted)
    # verify
    expected = [8, 9, 17, 19, 33, 39]
    pages = [item.page for item in extracted]
    assert pages == expected


@utilotest.nightly
def test_chapter_work_master98():
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    extracted = chapter(source)

    expected = [2, 6, 26, 42, 67, 85, 88, 96]
    pages = [item.page for item in extracted]

    assert pages == expected


@utilotest.longrun
def test_chapter_work_paper18():
    """Regression test to ensure that chapter start is detected."""
    source = hoverpower.link(hoverpower.PAPER018_PDF)
    extracted = chapter(source)

    expected = [1]  # extend after upgrader chapter parser
    pages = [item.page for item in extracted]

    assert pages == expected


def test_chapter_diss180_introduction():
    source = hoverpower.link(hoverpower.DISS180_PDF)
    extracted = chapter(source, pages=(18,))
    assert extracted[0].content.value >= 0.5


def test_chapter_diss266():
    source = hoverpower.link(hoverpower.DISS266_PDF)
    extracted = chapter(source, pages=(9,))
    assert extracted[0].content.value >= 0.5
