# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import configo
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


TITLE_LENGTH_MIN = configo.HV_INT_PLUS(default=10)

TITLE_LENGTH_MAX = configo.HV_INT_PLUS(default=200)

TITLE_CHARACTER_COUNT_MAX = configo.HV_INT_PLUS(default=1000)

EMPTY_RESULT = (0, 0.0)


def analyse_page(page: iamraw.Page, fontstore: iamraw.FontStore) -> float:
    """Determine the likelihood that `page` is a title page

    A high title_indicator provides a high likelihood of being a title
    page. Additionally the font_length_max is provided.

    Returns: (font_length_max, title_indicator):
    """
    pagenumber = page.page
    positions = font_positions_from_page(fontstore, pagenumber)
    fonts = font_sizes_from_page(fontstore, pagenumber)
    if returnvalue := no_titlepage(page, fonts):
        return returnvalue
    font_max, font_length_max = determine_hugest_font(fonts, positions, page)
    title_indicator = 0
    # the title must not be to short and it unlikeli that the title is very,
    # very long.
    # TODO: We need a concept for this "holy" values. Make them configurable
    if TITLE_LENGTH_MIN <= font_length_max < TITLE_LENGTH_MAX:
        title_indicator = font_length_max * pow(font_max, 3)
    # Malus per page, reduce value 10% per page, the higher the page number
    # the lower the likelihood to be the title page.
    # TODO: investigate if this is a good idea
    title_indicator = title_indicator * pow(0.10, pagenumber)
    # For high pages title_indicator produces very small number 10^-45. To
    # stabilize further algorithms, we do not want this "precision".
    title_indicator = utila.roundme(title_indicator)  # pylint:disable=R0204
    return font_length_max, title_indicator


def no_titlepage(page, fonts):
    if not fonts:  # empty page or page with images
        return EMPTY_RESULT
    numbers = sum((len(utila.parse_ints(str(item))) for item in page))
    if numbers > 70:
        # skip potential table of content page
        return EMPTY_RESULT
    character = len(''.join(line.text for line in page))
    if character > TITLE_CHARACTER_COUNT_MAX:
        # too many text content, this is not a title page
        return EMPTY_RESULT
    return None


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
    # font_max = max(fonts)
    # font_max_index = fonts.index(font_max)
    # text_length = [len(item) for item in texmex.split_page(page, positions)]
    # font_length_max = text_length[font_max_index]
    font_max, font_length_max = -utila.INF, -utila.INF
    for container in page:
        # TODO: MERGE EQUAL TEXT LINE TOGETHER?
        for line in container:
            fontsize = statistics.mean([char.size for char in line])
            if fontsize > font_max:
                font_max = fontsize
                font_length_max = len(line)
            if fontsize == font_max and len(line) > font_length_max:
                font_max = fontsize
                font_length_max = len(line)
    return font_max, font_length_max


def extract_titlelikelihood_frompath(
    path: str,
    pages: tuple = None,
) -> list[float]:
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
