# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import texmex
import utila
import utilatest

import sections.feature.whitepage

# CONTENT, BLANK, WHITE
RESTRUCT_EXPECTED = (
    [0, 2, 4, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26],
    [1],
    [3, 5, 7, 11, 19, 21, 23, 25],
)
# CONTENT, BLANK, WHITE
MASTER155_EXPECTED = (utila.rlist(155), [], [])
# CONTENT, BLANK, WHITE
# TODO IMPROVE AFTER FIXING WHITEPAGE EXTRACTOR
HC_DISS166_EXPECTED = ()


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.DOCU027_PDF, RESTRUCT_EXPECTED, id='docu27'),
    pytest.param(power.MASTER155_PDF, MASTER155_EXPECTED, id='master155'),
    pytest.param(power.HC_DISS166,
                 HC_DISS166_EXPECTED,
                 id='diss166hc',
                 marks=pytest.mark.xfail(reason='improve paper detector')),
])
@utilatest.nightly
def test_whitepages_extract_x(source, expected):
    utilatest.fixture_requires(source)
    result = whitepages(source)
    result = current(result)
    assert result == expected


BACHELOR090_EXPECTED = (
    [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 75,
        76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88
    ],
    [0, 89],
    [],
)


@utilatest.requires(power.BACHELOR090_PDF)
def test_document_whith_gaps():
    source = power.BACHELOR090_PDF
    result = whitepages(source)
    result = current(result)
    # adjust test after changing page numbers
    assert result == BACHELOR090_EXPECTED


def whitepages(document: str):
    source = power.link(document)
    navigators = serializeraw.ptn_frompath(
        source,
        state=texmex.TextState.ALL,
        fill_empty=False,
    )
    document = serializeraw.load_document(iamraw.path.text(source))

    headerfooters = utila.join(source, 'headnote__result_result.yaml')
    headerfooters = serializeraw.load_headerfooter(headerfooters)

    images, figures = sections.feature.whitepage.load_imagesfigures(
        images=utila.join(source, 'rawmaker__images_images'),
        figures=utila.join(source, 'rawmaker__figures_figures'),
        pages=None,
    )
    # work
    result = sections.feature.whitepage.extract_whitepages(
        document,
        navigators,
        headerfooters,
        images,
        figures,
    )
    return result


def current(items):
    content, blank, white = [], [], []
    for item in items:
        if item.content == sections.feature.whitepage.WhitePage.CONTENT:
            content.append(item.page)
        elif item.content == sections.feature.whitepage.WhitePage.BLANK:
            blank.append(item.page)
        elif item.content == sections.feature.whitepage.WhitePage.WHITE:
            white.append(item.page)
        else:
            raise ValueError(f'should not happen: {item}')
    return content, blank, white
