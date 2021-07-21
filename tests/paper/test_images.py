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

import sections.paper.rectangle


def test_image_frompdf():
    image = sections.paper.rectangle.image_frompdf(power.PAPER18_PDF, page=0)
    assert image


def test_image_bounding():
    image = sections.paper.rectangle.image_frompdf(power.PAPER18_PDF, page=1)
    boundings = sections.paper.rectangle.image_boundings(image)
    assert len(boundings) == 2
    # render detected boundings
    img = cv2.imread(image)
    sections.paper.rectangle.image_render_rectangle(img, boundings)
    cv2.imwrite(image, img)
