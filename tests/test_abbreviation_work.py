# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
def test_abbreviations_bachelor37_work():
    pages = (0, 1, 2, 5, 6)
    source = power.BACHELOR037_PDF
    extracted = abbreviations(source, pages)
    selected = utila.select_page(extracted, page=1)
    assert selected.content.value >= 0.8, str(selected)


def test_abbreviations_diss170_work():
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


def abbreviations(source, pages):
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
