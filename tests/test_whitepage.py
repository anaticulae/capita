# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw.path
import power
import pytest
import serializeraw
import serializeraw.images
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
MASTER155_EXPECTED = (utila.ranged_list(0, 155), [], [])


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


def whitepages(document: str):
    source = power.link(document)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    document = serializeraw.load_document(iamraw.path.text(source))

    headerfooters = iamraw.path.headerfooters(source)
    headerfooters = serializeraw.load_headerfooter(headerfooters)

    images = serializeraw.images.load_image_informations_frompath(
        os.path.join(
            source,
            'rawmaker__images_images',
        ))
    figures = serializeraw.images.load_image_informations_frompath(
        os.path.join(
            source,
            'rawmaker__figures_figures',
        ))

    # work
    result = sections.feature.whitepage.extract_whitepages(
        document,
        navigators,
        headerfooters,
        images,
        figures,
    )
    return result


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.DOCU027_PDF, RESTRUCT_EXPECTED, id='docu27'),
    pytest.param(power.MASTER155_PDF, MASTER155_EXPECTED, id='master155'),
])
@utilatest.nightly
def test_whitepages_extract_x(source, expected):
    utilatest.fixture_requires(source)
    result = whitepages(source)
    result = current(result)
    assert result == expected
