# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Whitepage Extractor
===================

use footer and header to detect white pages

3 types of white pages:

    - complete white: blank page
    - white page with footer and or header
    - content: that's not a whitepage

required resources:

    - text
    - position
    - footer

"""

import collections
import enum

import iamraw
import serializeraw
import serializeraw.images
import texmex
import utilo

PageContentWhitepages = collections.namedtuple(
    'PageContentWhitepages',
    'content, page',
)


class WhitePage(enum.Enum):
    CONTENT = -1
    BLANK = 0  # nothing on the page
    WHITE = 1  # page with footer and/or header


def work(
    document: str,
    position: str,
    footers: str,
    images: str = None,
    figures: str = None,
    pages=None,
) -> str:
    """Extract `WhitePage` out of document.

    There are three types of `Whitepage`: BLANK, WHITE AND CONTENT

    Args:
        document(path): path to document text
        position(path): path to document text positions
        footers(path): path to extract footers
        images(path): path to images
        figures(path): path to figures
        pages(list): select `pages` to load
    Returns:
        dumped `yaml` result of extracted whitepages
    """
    pages = utilo.ensure_tuple(pages)
    # load
    document = serializeraw.load_document(document, pages=pages)
    position = serializeraw.load_textpositions(position, pages=pages)
    headerfooters = serializeraw.load_headerfooter(
        footers,
        pages=pages,
    )
    navigators = texmex.create_ptns(
        text=document,
        textpositions=position,
        state=texmex.TextState.ALL,
        fill_empty=False,
    )
    images, figures = load_imagesfigures(images, figures, pages)
    # work
    extracted = extract_whitepages(
        document,
        navigators,
        headerfooters,
        images,
        figures,
    )
    dumped = serializeraw.dump_whitepages(extracted)
    return dumped


def load_imagesfigures(images, figures, pages):
    images = images if isinstance(images, str) else images[0]
    figures = figures if isinstance(images, str) else figures[0]
    if images and utilo.exists(images):
        images = serializeraw.images.load_image_informations_frompath(
            images,
            pages=pages,
        )
    else:
        utilo.debug(f'no images: {images}')
        images = None
    if figures and utilo.exists(figures):
        figures = serializeraw.images.load_image_informations_frompath(
            figures,
            pages=pages,
        )
    else:
        utilo.debug(f'no figures: {figures}')
        figures = None
    return images, figures


def extract_whitepages(  # pylint:disable=R0914
    document: iamraw.Document,
    navigators: texmex.PTNs,
    headerfooters,
    images: list = None,
    figures: list = None,
):
    images = images if images else []
    figures = figures if figures else []
    result = {}
    for pagenumber, data in utilo.sync_pages([
            document,
            navigators,
            headerfooters,
            images,
            figures,
    ]):
        currentpage, navigator, headerfooter, figure, image = data
        noimage = not image and not figure
        nocontent = not navigator and noimage
        header, footer = None, None
        if headerfooter:
            header, footer = headerfooter.header, headerfooter.footer
        if nocontent:
            result[pagenumber] = WhitePage.BLANK
            continue
        if not header and not footer:
            if currentpage and not currentpage.children and noimage:
                result[pagenumber] = WhitePage.BLANK
            else:
                # Elements on the page, maybe title page, chapter page...
                result[pagenumber] = WhitePage.CONTENT
        else:
            top = header.end if header else texmex.START
            bottom = footer.begin if footer else texmex.END
            if not navigator.between(top, bottom) and noimage:
                result[pagenumber] = WhitePage.WHITE
            else:
                # page with footer and/or header and content - "normal page"
                result[pagenumber] = WhitePage.CONTENT
    # convert
    result = [
        PageContentWhitepages(
            page=page,
            content=WhitePage[whitepage.name] if whitepage else None,
        ) for page, whitepage in result.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result
