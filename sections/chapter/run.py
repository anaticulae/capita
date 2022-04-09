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
        if nochapter(page):
            continue
        # prepare content
        pagestart = page.between(AFTER_HEADER, FIRST_QUARTER)
        # run strategies
        rate = sections.chapter.starter.contain_chapter(pagestart)
        rate += sections.chapter.outlines.rate_from_outlines(
            outlines,
            pagestart,
        )
        if rate <= 0.0:
            # TODO: VERY VERBOSE, CHECK LATER
            utila.verbose(f'    no chapter {page.page}: chapterate {rate}')
            continue
        # convert result to percents
        rate_in_percent = chaptervalue_to_percent(rate, outlines)
        result.append(
            iamraw.PageContentLikelihood(
                page=page.page,
                content=iamraw.Likelihood(rate_in_percent, 'chapter'),
            ))
        # TODO: There is the possiblity that header and start of chapter
        # are together, support later
        # result.append(0.0)
    return result


def nochapter(page) -> bool:
    if not page:
        # empty page
        return True
    if page.rotated:
        utila.verbose(f'no chapter {page.page}: rotated')
        return True
    pagestart = page.between(AFTER_HEADER, FIRST_QUARTER)
    if no_textcontent(pagestart):
        utila.verbose(f'no chapter {page.page}: no textcontent')
        return True
    if contains_listof(pagestart):
        if not sections.chapter.starter.startwith_hugenumber(pagestart):
            utila.verbose(f'no chapter {page.page}: list of dots')
            # TODO: See todo below XXX???
            # chapter_rate = 0
            return True
    return False


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


def contains_listof(content: list) -> bool:
    raw = rawcontent(content)
    dots_with_spaces = raw.count('. . . .')
    connected_dots = raw.count('....')
    result = dots_with_spaces > 4 or connected_dots >= 3
    return result


def rawcontent(content) -> str:
    raw = utila.NEWLINE.join([item.text for item in content])
    raw = raw.lower()
    return raw
