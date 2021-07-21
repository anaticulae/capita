# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import cv2
import pdfinfo.pages
import utila

import sections.paper.rectangle


def percentage(path: str, pages: tuple = None) -> tuple:
    utila.exists_assert(path)
    pdfpages = pdfinfo.pages.determine(path)
    collected = []
    for page in range(pdfpages):
        if utila.should_skip(page, pages):
            continue
        image = sections.paper.rectangle.image_frompdf(path, page)
        boundings = sections.paper.rectangle.image_boundings(image)
        img = cv2.imread(image)
        sections.paper.rectangle.image_render_rectangle(img, boundings)
        collected.append(boundings)
        cv2.imwrite(image, img)
    result = tuple(double_column(page) for page in collected)
    return result


def double_column(boundings, stepsize=5.0) -> float:  # pylint:disable=R0914
    """\
    >>> double_column(((0, 2, 500, 250), (0, 270, 250, 400), (290, 270, 500, 400)), stepsize=5.0)
    0.33
    """
    if not boundings:
        return None
    # remove yoffset to ignore space before first rectangle
    y0 = min(item[1] for item in boundings)
    boundings = [
        (item[0], item[1] - y0, item[2], item[3] - y0) for item in boundings
    ]
    width = max(item[2] for item in boundings)
    height = max(item[3] for item in boundings)
    center_left = width * 0.40
    center_right = width * 0.60
    normal = []
    double = []
    for x0, y0, x1, y1 in boundings:
        doubled = (x1 < center_right or x0 > center_left)
        if x0 < center_left and x1 > center_right:
            doubled = False
        for yn in utila.ranges(start=y0, stop=y1, step=stepsize):  # pylint:disable=C0103
            yn = int(yn / 5) * 5  # pylint:disable=C0103
            if doubled:
                double.append(yn)
            else:
                normal.append(yn)
    double, normal = utila.make_unique(double), utila.make_unique(normal)
    double = [item for item in double if item not in normal]
    double = utila.groupby_diff(double, diff=stepsize * 2)
    double.sort()
    normal.sort()
    doubled = 0.0
    percent = 1.0 / height
    for item in double:
        start, end = item[0], item[-1]
        doubled += percent * (end - start)
    doubled: float = utila.roundme(doubled)
    return doubled
