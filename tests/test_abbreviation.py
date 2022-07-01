# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import sections.feature.abbreviation


@utilatest.longrun
def test_abbrev_bachelor37_work():
    pages = (0, 1, 2, 5, 6)
    source = power.BACHELOR037_PDF
    extracted = abbreviations(source, pages)
    selected = utila.select_page(extracted, page=1)
    assert selected.content.value >= 0.8, str(selected)


@utilatest.longrun
def test_abbrev_diss170_work():
    pages = (141, 142)
    source = power.DISS170_PDF
    extracted = abbreviations(source, pages)
    selected = utila.select_pages(extracted, pages=pages)
    current = [item.content.value >= 0.6 for item in selected]
    assert current == [True, True], str(selected)


def test_no_abbreviations_master72_page9():
    source = power.MASTER072_PDF
    page = 9
    extracted = abbreviations(source, page)
    selected = utila.select_page(extracted, page=page)
    assert not selected.content.value


def test_no_abbreviations_bachelor241_page75():
    source = power.BACHELOR241_PDF
    page = 75
    extracted = abbreviations(source, pages=page)
    selected = utila.select_page(extracted, page=page)
    assert not selected.content.value
    assert not sum(item.content.value for item in extracted)


def test_no_abbreviations_bachelor111page56():
    """Code was parsed as double column which was detected as
    abbreviation back page."""
    extracted = abbreviations(power.BACHELOR111_PDF, pages=56)
    assert not extracted[0].content.value


@utilatest.nightly
def test_no_abbreviations_master193():
    extracted = abbreviations(power.MASTER193_PDF)
    pages = [item.content.value for item in extracted]
    assert not any(pages)


@utilatest.longrun
def test_abbrev_diss167_four_pages():
    extracted = abbreviations(
        power.DISS167_PDF,
        pages=utila.rlist(10, 20),
    )
    pages = [item.page for item in extracted if item.content.value]
    expected = [11, 12, 13, 14, 15, 16]
    assert pages == expected


@utilatest.longrun
def test_abbrev_diss406():
    extracted = abbreviations(
        power.DISS406_PDF,
        pages=utila.rlist(30),
    )
    pages = [item.page for item in extracted if item.content.value]
    expected = utila.rlist(13, 22)
    assert pages == expected


def abbreviations(source, pages=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    extracted = sections.feature.abbreviation.work(
        text,
        textposition,
        pages=pages,
    )
    loaded = serializeraw.load_likelihood(extracted)
    return loaded
