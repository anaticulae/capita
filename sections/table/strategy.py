# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import elements
import iamraw
import serializeraw
import texmex
import utila

import sections.feature
import sections.utils.headline

NO_PAGE = (0, 0)


def work(
        navigators: texmex.PageTextContentNavigators,
        headline: str,
        shortcut: str,
        pages: tuple = None,
        noheadlines: list = None,
        second: bool = False,
        pattern: callable = None,
) -> str:
    extracted = extract_xxx_likelihood(
        navigators,
        headline,
        shortcut=shortcut,
        pages=pages,
        noheadlines=noheadlines,
        pattern=pattern,
    )
    if second:
        # disable required headline to merge table pages which follows
        # start page.
        without = extract_xxx_likelihood(
            navigators,
            headline=None,
            shortcut=shortcut,
            noheadlines=noheadlines,
            pages=pages,
            pattern=pattern,
        )
        extracted = merge_second(extracted, without)

    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


def extract_xxx_likelihood(
        document: texmex.PageTextContentNavigators,
        headline: str = None,
        shortcut: str = 'xxx',
        pages: tuple = None,
        noheadlines: list = None,
        pattern: callable = None,
) -> iamraw.PageContentLikelihood:
    """Iterate thru document and determine uni- or multi formed
    likelihood of being a table page."""
    result = {
        page.page: (page, analyse_page(page, pattern)) for page in document
    }

    result = {
        page: judged if not utila.should_skip(page, pages) and
        matched(content, headline, noheadlines) else NO_PAGE
        for page, (content, judged) in result.items()
    }
    uniformed = sections.feature.uniform_result(result)
    multiformed = sections.feature.multiform_result(result)

    uniformed = multiformed if multiformed else uniformed
    assert len(uniformed) == len(document)

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, name=shortcut),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result


def matched(navigator, headline, noheadlines) -> bool:
    """Collect headlines from `navigator` and check if given `headline`
    is found and colected headline is not `noheadlines`."""
    detected = sections.utils.headline.headlines(navigator, topsearch=True)
    if noheadlines and detected in noheadlines:
        return False
    if not headline:
        # disable headline check, use noheadline to skip false positive
        # matches. False positive is detected when table of figure follow
        # a table of content for example.
        return True
    if detected and headline:
        if isinstance(headline, str):
            return detected == headline
        return detected in headline
    return False


def analyse_page(content, pattern: callable = None) -> float:
    """Extract the number of lines which can contain any table-content

    Dots(. . .) are charactaristical for table lines.

    Args:
        page():
    Returns:
        (linecount, possible_table_lines)
    """
    valid = valid_line if not pattern else lambda x: valid_line(x) or pattern(x)
    linecount = len(content)
    possible_toc_line = len([line for line in content if valid(line.text)])
    return linecount, possible_toc_line


def valid_line(line: str) -> bool:
    if line.count('. .') > 3:
        return True
    if line.count('..') > 3:
        return True
    if elements.level_numbered(line):
        return True
    return False


def merge_second(extracted, without, min_merge=0.5):
    """Merge following table pages which follows `extracted` first
    table. Break merging after detecting first empty page."""
    # TODO: DIRTY
    start = -1
    for index, item in enumerate(extracted):
        if item.content.value == 1.0:
            start = index
            break
    if start == -1:
        return extracted
    start += 1
    for index, item in enumerate(without[start:], start=start):
        if item.content.value <= 0.5:
            break
        # update value of first extraction
        extracted[index].content.value = item.content.value
    return extracted
