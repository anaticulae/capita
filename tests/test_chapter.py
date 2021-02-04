# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import sections.feature.chapter


# TODO: DISS266 - IMPROVE LATER
@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.DOCU27_PDF,
        [6, 8, 10, 12, 18, 20, 22, 24],
        id='restruct',
    ),
    pytest.param(
        power.MASTER072_PDF,
        [3, 6, 22, 45, 63],
        id='master72pages',
    ),
    pytest.param(
        power.DISS266_PDF,
        [4, 5, 9, 23, 81, 103, 136, 197, 203, 205, 253],
        id='diss266',
    ),
])
@utilatest.nightly
def test_chapter_extract(source, expected):
    source = power.link(source)
    # run
    result = extract_chapter(source)
    # verify result
    pages = [item.page for item in result]
    assert pages == expected


def test_chapter_dump_and_load_detection():
    source = power.link(power.DOCU27_PDF)

    result = extract_chapter(source)

    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)
    assert loaded == result


def extract_chapter(source):
    # load
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    tocs = serializeraw.load_toc(iamraw.path.text(source))
    # run
    result = sections.feature.chapter.extract_chapter(
        navigators,
        tocs,
    )
    return result


def chapter(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    dumped = sections.feature.chapter.work(
        document=source,  # use default path
        position=source,
        tocpath=source,
        pages=pages,
    )
    assert dumped, dumped
    loaded = serializeraw.load_likelihood(dumped)
    return loaded


def test_chapter_work_bachelor63():
    source = power.link(power.BACHELOR063_PDF)
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


@utilatest.longrun
def test_chapter_work_master98():
    source = power.link(power.MASTER098_PDF)
    extracted = chapter(source)

    expected = [2, 6, 26, 42, 67, 85, 88, 96]
    pages = [item.page for item in extracted]

    assert pages == expected


def test_chapter_work_paper18():
    """Regression test to ensure that chapter start is detected."""
    source = power.link(power.PAPER18_PDF)
    extracted = chapter(source)

    expected = [1]  # extend after upgrader chapter parser
    pages = [item.page for item in extracted]

    assert pages == expected
