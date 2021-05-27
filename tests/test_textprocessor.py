# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: REMOVE/MOVE TO TEXMEX

import iamraw
import iamraw.path
import power
from serializeraw import load_document
from serializeraw import load_font_content
from serializeraw import load_font_header
from texmex.iter import PageIter

from sections.feature.title import font_positions_from_page


def pyporting_pages(pagenumber: int):
    docu09 = power.link(power.DOCU09_PDF)
    document = load_document(iamraw.path.text(docu09))
    current_page = document[pagenumber]

    header = load_font_header(iamraw.path.fontheader(docu09))

    content = load_font_content(iamraw.path.fontcontent(docu09))
    fontstore = iamraw.FontStore(header, content)

    positions = font_positions_from_page(fontstore, pagenumber)

    pageiter = PageIter(page=current_page)
    return pageiter, positions


def test_textprocessor_example_pyporting_page_2():
    pageiter, positions = pyporting_pages(2)

    result = []
    for item in positions:
        extracted = pageiter.next_item(*item).strip()
        result.append(extracted)
