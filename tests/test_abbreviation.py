# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilo
import utilotest

import sections.feature.abbreviation


@utilotest.longrun
def test_abbrev_bachelor37_work():
    pages = (0, 1, 2, 5, 6)
    source = hoverpower.BACHELOR037_PDF
    extracted = abbreviations(source, pages)
    selected = utilo.select_page(extracted, page=1)
    assert selected.content.value >= 0.8, str(selected)


@utilotest.longrun
def test_abbrev_diss170_work():
    pages = (141, 142)
    source = hoverpower.DISS170_PDF
    extracted = abbreviations(source, pages)
    selected = utilo.select_pages(extracted, pages=pages)
    current = [item.content.value >= 0.6 for item in selected]
    assert current == [True, True], str(selected)


def test_no_abbreviations_master72_page9():
    source = hoverpower.MASTER072_PDF
    page = 9
    extracted = abbreviations(source, page)
    selected = utilo.select_page(extracted, page=page)
    assert not selected.content.value


def test_no_abbreviations_bachelor241_page75():
    source = hoverpower.BACHELOR241_PDF
    page = 75
    extracted = abbreviations(source, pages=page)
    selected = utilo.select_page(extracted, page=page)
    assert not selected.content.value
    assert not sum(item.content.value for item in extracted)


def test_no_abbreviations_bachelor111page56():
    """Code was parsed as double column which was detected as
    abbreviation back page."""
    extracted = abbreviations(hoverpower.BACHELOR111_PDF, pages=56)
    assert not extracted[0].content.value


@utilotest.nightly
def test_no_abbreviations_master193():
    extracted = abbreviations(hoverpower.MASTER193_PDF)
    pages = [item.content.value for item in extracted]
    assert not any(pages)


@utilotest.longrun
def test_abbrev_diss167_four_pages():
    extracted = abbreviations(
        hoverpower.DISS167_PDF,
        pages=utilo.rlist(10, 20),
    )
    pages = [item.page for item in extracted if item.content.value]
    expected = [11, 12, 13, 14, 15, 16]
    assert pages == expected


@utilotest.longrun
def test_abbrev_diss406():
    extracted = abbreviations(
        hoverpower.DISS406_PDF,
        pages=utilo.rlist(30),
    )
    pages = [item.page for item in extracted if item.content.value]
    expected = utilo.rlist(13, 22)
    assert pages == expected


def test_abbrev_bachelor090():
    extracted = abbreviations(hoverpower.BACHELOR090_PDF)
    pages = [item.page for item in extracted if item.content.value]
    expected = [10, 11]
    assert pages == expected


def abbreviations(source, pages=None):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    extracted = sections.feature.abbreviation.work(
        text,
        textposition,
        pages=pages,
    )
    loaded = serializeraw.load_likelihood(extracted)
    return loaded
