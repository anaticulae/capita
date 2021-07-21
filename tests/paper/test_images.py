# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import cv2
import power
import pytest

import sections.paper.rectangle


def test_image_frompdf():
    image = sections.paper.rectangle.image_frompdf(power.PAPER18_PDF, page=0)
    assert image


@pytest.mark.parametrize(
    'source, page, expected',
    [
        pytest.param(power.PAPER18_PDF, 1, 1, id='paper18page1'),
        pytest.param(power.PAPER14_PDF, 10, 9, id='paper14page10'),
    ],
)
def test_image_bounding(source, page, expected):
    image = sections.paper.rectangle.image_frompdf(source, page=page)
    boundings = sections.paper.rectangle.image_boundings(image)
    # render detected boundings
    img = cv2.imread(image)
    img = sections.paper.rectangle.image_render_rectangle(img, boundings)
    cv2.imwrite(image, img)
    assert len(boundings) == expected
