# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import configo
import iamraw
import texmex
import utila

import sections.chapter.outlines
import sections.chapter.starter

AFTER_HEADER = configo.HV_PERCENT_PLUS(default=5.0)

FIRST_QUARTER = configo.HV_PERCENT_PLUS(default=45.0)


def extract_chapter(
    navigators: texmex.PageTextNavigators,
    outlines,
) -> iamraw.PageContentLikelihoods:
    result = []
    for page in navigators:
        if not page:
            # empty page
            continue
        if page.rotated:
            utila.debug(f'no chapter {page.page}: rotated')
            continue
        first_content = page.between(AFTER_HEADER, FIRST_QUARTER)
        if no_textcontent(first_content):
            utila.debug(f'no chapter {page.page}: no textcontent')
            continue
        chapter_rate = sections.chapter.starter.contain_chapter(first_content)
        chapter_rate += sections.chapter.outlines.rate_from_outlines(
            outlines,
            first_content,
        )
        if contains_listof(first_content):
            utila.debug(f'no chapter {page.page}: list of dots')
            # TODO: See todo below
            chapter_rate = 0
        if chapter_rate <= 0.0:
            continue
        rate_in_percent = chaptervalue_to_percent(chapter_rate, outlines)
        result.append(
            iamraw.PageContentLikelihood(
                page=page.page,
                content=iamraw.Likelihood(rate_in_percent, 'chapter'),
            ))
        # TODO: There is the possiblity that header and start of chapter
        # are together, support later
        # result.append(0.0)
    return result


def no_textcontent(content: list) -> bool:
    """A chapter start requires some text line at the start.

    This is required to skip false positive chapter starts which are
    just a table or so.
    """
    if len(content) < 5:
        return False
    avg = statistics.mean((len(item.text) for item in content))
    if avg < 35:
        # TODO: HOLY VALUE
        return True
    return False


def chaptervalue_to_percent(chaptervalue: float, hastoc: bool) -> float:
    """Convert `chaptervalue` to percent.

    Args:
        chaptervalue(float): value of detected features
        hastoc(bool): if no toc is provided, some features can not be
                       processed.
    Returns:
        Likelihood of beeing a chapter start.?
    """
    # TODO: HOLY VALUES
    # TODO: IMPROVE THIS CONCEPT
    if not hastoc and chaptervalue >= 1.0:
        return 1.0
    if chaptervalue >= 2.5:
        return 1.0
    if chaptervalue >= 0.5:
        return 0.5
    return 0.0


def contains_listof(content: str) -> bool:
    raw = rawcontent(content)
    dots_with_spaces = raw.count('. . . .')
    connected_dots = raw.count('....')
    result = dots_with_spaces > 4 or connected_dots >= 3
    return result


def rawcontent(content) -> str:
    raw = utila.NEWLINE.join([item.text for item in content])
    raw = raw.lower()
    return raw
