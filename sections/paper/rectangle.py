# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import cv2
import utila

import sections

GHOST = 'gswin64c' if os.name == 'nt' else 'gs'


def image_frompdf(pdf: str, page: int) -> str:
    tmpdir = utila.tmpdir(sections.ROOT)
    outpath = utila.forward_slash(
        os.path.join(tmpdir, f'image-{page}.png'),
        newline=True,
    )
    config = '-q -sDEVICE=png16m -r300 -dBATCH -dNOPAUSE -SAFE'
    call = f'{GHOST} {config} -sPageList={page+1} -o {outpath} {pdf}'
    utila.run(call)
    return outpath


RECTANGLE_SIZE_MIN = 150  # TODO: HOLY VALUE


def image_boundings(image: str) -> list:
    utila.exists_assert(image)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=191,
        C=-11,
    )
    # determine contours
    contours, __ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # merge contour to maximized rectangle
    result = []
    for group in contours:
        items = [item[0] for item in group]
        x = [item[0] for item in items]
        y = [item[1] for item in items]
        xleft, xright = min(x), max(x)
        ytop, ybottom = min(y), max(y)
        rectangle = (xleft, ytop, xright, ybottom)
        if utila.rectangle_size(rectangle) < RECTANGLE_SIZE_MIN:
            continue
        result.append(rectangle)
    return result


def image_render_rectangle(image, boundings: tuple):
    for bounding in boundings:
        xleft, ytop, xright, ybottom = bounding
        cv2.rectangle(
            image,
            (xleft, ytop),
            (xright, ybottom),
            (255, 100, 100),
            10,
        )
    return image
