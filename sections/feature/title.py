# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics
import typing

import iamraw
import serializeraw
import utila

import sections.feature


def work(
        text_linewise: str,
        font_header: str,
        font_content: str,
        pages=None,
) -> str:
    document = serializeraw.load_document(text_linewise, pages=pages)

    lookup = serializeraw.create_fontstore(font_header, font_content)

    result = extract_title_likelihood(document, lookup)
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def extract_title_likelihood(
        document: iamraw.Document,
        fontstore: iamraw.FontStore,
) -> iamraw.PageContentLikelihood:
    result = {page.page: analyse_page(page, fontstore) for page in document}

    uniformed = sections.feature.uniform_result(result)

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, 'title'),
        ) for page, value in uniformed.items()
    ]
    return result


MINIMAL_TITLE_LENGTH = 10  # TODO: CONVERT TO HOLY VALUE
MAXIMAL_TITLE_LENGTH = 200

EMPTY_RESULT = (0, 0.0)


def analyse_page(page: iamraw.Page, fontstore: iamraw.FontStore) -> float:
    """Determine the likelihood that `page` is a title page

    A high title_indicator provides a high likelihood of beeing a title
    page. Aditionally the max_font_length is provided.

    Returns: (max_font_length, title_indicator):
    """
    pagenumber = page.page
    positions = font_positions_from_page(fontstore, pagenumber)
    fonts = font_sizes_from_page(fontstore, pagenumber)

    if not fonts:  # empty page or page with images
        return EMPTY_RESULT

    numbers = sum([len(utila.parse_numbers(str(item))) for item in page])
    if numbers > 70:
        # skip potential table of content page
        return EMPTY_RESULT

    max_font, max_font_length = determine_hugest_font(fonts, positions, page)
    title_indicator = 0
    # the title must not be to short and it unlikeli that the title is very,
    # very long.
    # TODO: We need a concept for this "holy" values. Make them configurable
    if MINIMAL_TITLE_LENGTH <= max_font_length < MAXIMAL_TITLE_LENGTH:
        title_indicator = max_font_length * pow(max_font, 3)
    # Malus per page, reduce value 10% per page, the higher the page number
    # the lower the likelihood to be the title page.
    # TODO: investigate if this is a good idea
    title_indicator = title_indicator * pow(0.10, pagenumber)
    # For high pages title_indicator produces very small number 10^-45. To
    # stabilize further algorithms, we do not want this "precision".
    title_indicator = utila.roundme(title_indicator)  # pylint:disable=R0204
    return max_font_length, title_indicator


def font_sizes_from_page(store: iamraw.FontStore, pagenumber: int):
    fonts = []
    for _, __, ___, font in store.page_iter(pagenumber):
        try:
            fonts.append(store[font].scale)
        except KeyError:
            utila.error(f'missing font key: {font}')
    return fonts


def font_positions_from_page(store: iamraw.FontStore, pagenumber: int):
    positions = [(
        container,
        line,
        char,
    ) for container, line, char, _ in store.page_iter(pagenumber)]
    return positions


def determine_hugest_font(fonts, positions, page: iamraw.Page):  # pylint:disable=W0613
    """Determine the biggest font size."""
    # TODO: USE OLD APPROACH?
    # max_font = max(fonts)
    # max_font_index = fonts.index(max_font)
    #
    # text_length = [len(item) for item in texmex.split_page(page, positions)]
    # max_font_length = text_length[max_font_index]
    max_font, max_font_length = -utila.INF, -utila.INF
    for container in page:
        # TODO: MERGE EQUAL TEXT LINE TOGETHER?
        for line in container:
            fontsize = statistics.mean([char.size for char in line])
            if fontsize > max_font:
                max_font = fontsize
                max_font_length = len(line)
            if fontsize == max_font and len(line) > max_font_length:
                max_font = fontsize
                max_font_length = len(line)
    return max_font, max_font_length


def extract_titlelikelihood_frompath(
        path: str,
        pages: tuple = None,
) -> typing.List[float]:
    document = serializeraw.load_document(iamraw.path.text(path), pages=pages)
    fontstore = serializeraw.create_fontstore(
        iamraw.path.fontheader(path),
        iamraw.path.fontcontent(path),
        pages=pages,
    )
    result = sections.feature.title.extract_title_likelihood(
        document,
        fontstore,
    )
    return result
