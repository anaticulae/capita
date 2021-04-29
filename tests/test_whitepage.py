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
import serializeraw

from sections.feature.whitepage import PageContentWhitepages
from sections.feature.whitepage import WhitePage
from sections.feature.whitepage import extract_whitepages

# CONTENT, BLANK, WHITE
RESTRUCT_EXPECTED = (
    [0, 2, 4, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26],
    [1],
    [3, 5, 7, 11, 19, 21, 23, 25],
)


def current(items):
    content, blank, white = [], [], []
    for item in items:
        if item.content == WhitePage.CONTENT:
            content.append(item.page)
        elif item.content == WhitePage.BLANK:
            blank.append(item.page)
        elif item.content == WhitePage.WHITE:
            white.append(item.page)
        else:
            raise ValueError(f'should not happen: {item}')
    return content, blank, white


def whitepages(document: str):
    source = power.link(document)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    document = serializeraw.load_document(iamraw.path.text(source))

    headerfooters = iamraw.path.headerfooters(source)
    headerfooters = serializeraw.load_headerfooter(headerfooters)

    # work
    result = extract_whitepages(document, navigators, headerfooters)
    return result


def test_whitepages_extract():
    result = whitepages(power.DOCU27_PDF)
    result = current(result)
    # convert dict to list
    assert result == RESTRUCT_EXPECTED
