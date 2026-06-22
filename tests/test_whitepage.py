# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita.feature.whitepage
import hoverpower
import iamraw.path
import pytest
import serializeraw
import texmex
import utilo
import utilotest

# CONTENT, BLANK, WHITE
RESTRUCT_EXPECTED = (
    [0, 2, 4, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26],
    [1],
    [3, 5, 7, 11, 19, 21, 23, 25],
)
# CONTENT, BLANK, WHITE
MASTER155_EXPECTED = (utilo.rlist(155), [], [])
# CONTENT, BLANK, WHITE
# TODO IMPROVE AFTER FIXING WHITEPAGE EXTRACTOR
HC_DISS166_EXPECTED = ()


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        hoverpower.DOCU027_PDF,
        RESTRUCT_EXPECTED,
        id='docu27',
        marks=pytest.mark.xfail(reason='complete integration'),
    ),
    pytest.param(hoverpower.MASTER155_PDF, MASTER155_EXPECTED, id='master155'),
    pytest.param(hoverpower.HC_DISS166,
                 HC_DISS166_EXPECTED,
                 id='diss166hc',
                 marks=pytest.mark.xfail(reason='improve paper detector')),
])
@utilotest.nightly
def test_whitepages_extract_x(source, expected):
    utilotest.fixture_requires(source)
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


@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_document_whith_gaps():
    source = hoverpower.BACHELOR090_PDF
    result = whitepages(source)
    result = current(result)
    # adjust test after changing page numbers
    assert result == BACHELOR090_EXPECTED


def whitepages(document: str):
    source = hoverpower.link(document)
    navigators = serializeraw.ptn_frompath(
        source,
        state=texmex.TextState.ALL,
        fill_empty=False,
    )
    document = serializeraw.load_document(iamraw.path.text(source))

    headerfooters = utilo.join(source, 'headnote__result_result.yaml')
    if utilo.exists(headerfooters):
        headerfooters = serializeraw.load_headerfooter(headerfooters)
    else:
        headerfooters = iamraw.PageContentFooterHeaders(content=[])

    images, figures = capita.feature.whitepage.load_imagesfigures(
        images=utilo.join(source, 'rawmaker__images_images'),
        figures=utilo.join(source, 'rawmaker__figures_figures'),
        pages=None,
    )
    # work
    result = capita.feature.whitepage.extract_whitepages(
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
        if item.content == capita.feature.whitepage.WhitePage.CONTENT:
            content.append(item.page)
        elif item.content == capita.feature.whitepage.WhitePage.BLANK:
            blank.append(item.page)
        elif item.content == capita.feature.whitepage.WhitePage.WHITE:
            white.append(item.page)
        else:
            raise ValueError(f'should not happen: {item}')
    return content, blank, white
