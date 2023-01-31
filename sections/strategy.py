# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import serializeraw
import texmex
import utila

import sections.feature
import sections.utils.headline

HEADLINE_COLLECT_MIN = configo.HV_FLOAT_PLUS(default=0.85, limit=1.0)
NOHEADLINE_COLLECT_MIN = configo.HV_FLOAT_PLUS(default=0.85, limit=1.0)


def work(
    navigators: texmex.PTCNs,
    headline: str,
    shortcut: str,
    pages: tuple = None,
    noheadlines: list = None,
    *,
    second: bool = False,
    topsearch: bool = True,
    pattern: callable = None,
) -> str:
    extracted = extract_xxx_likelihood(
        navigators,
        headline,
        shortcut=shortcut,
        pages=pages,
        noheadlines=noheadlines,
        pattern=pattern,
        topsearch=topsearch,
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
            topsearch=topsearch,
        )
        extracted = merge_second(
            extracted,
            without,
            title=shortcut,
        )
    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


def extract_xxx_likelihood(
    document: texmex.PTCNs,
    headline: str = None,
    shortcut: str = 'xxx',
    pages: tuple = None,
    noheadlines: list = None,
    pattern: callable = None,
    likelihood_min: float = 0.2,
    topsearch: bool = True,
) -> iamraw.PageContentLikelihood:
    """Iterate thru document and determine uni- or multi formed
    likelihood of being a table page."""
    result = {
        page.page: (page, analyse_page(page, pattern)) for page in document
    }
    result = {
        page: judged if not utila.should_skip(page, pages) and
        matched(content, headline, noheadlines, topsearch=topsearch) else
        sections.feature.NO_PAGE for page, (content, judged) in result.items()
    }
    uniformed = sections.feature.uniform_result(result)
    multiformed = sections.feature.multiform_result(result)
    uniformed = multiformed if multiformed else uniformed
    assert len(uniformed) == len(document)

    uniformed = {
        page: 0.0 if value < likelihood_min else value
        for page, value in uniformed.items()
    }

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, name=shortcut),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result


def matched(
    navigator,
    headline,
    noheadlines,
    *,
    topsearch: bool = True,
) -> bool:
    """Collect headlines from `navigator` and check if given `headline`
    is found and collected headline is not `noheadlines`.
    """
    detected = sections.utils.headline.headlines(navigator, topsearch=topsearch)
    if noheadlines and detected:
        if utila.similar(noheadlines, detected, maxdiff=HEADLINE_COLLECT_MIN):
            return False
    if not headline:
        # disable headline check, use noheadline to skip false positive
        # matches. False positive is detected when table of figure follow
        # a table of content for example.
        return True
    if detected and headline:
        if utila.similar(headline, detected, maxdiff=NOHEADLINE_COLLECT_MIN):
            return True
    return False


def analyse_page(content, pattern: callable) -> float:
    """Extract the number of lines which can contain any table-content

    Dots(. . .) are charactaristical for table lines.

    Args:
        page():
    Returns:
        (linecount, possible_table_lines)
    """
    # remove lines which are too short
    content = [line for line in content if len(line.text.strip()) >= 5]
    linecount = len(content)
    possible_toc_line = len([line for line in content if pattern(line.text)])
    return linecount, possible_toc_line


def merge_second(
    extracted,
    without,
    merge_min=0.5,
    replace=None,
    title: str = 'toc',
) -> list:
    """Merge following table pages which follows `extracted` first table.

    Break merging after detecting first empty page.
    """
    # TODO: DIRTY
    start = -1
    for index, item in enumerate(extracted):
        if item.content.value == 1.0:
            start = index
            break
    if start == -1:
        utila.debug(f'could not find {title} start; merge_second not possible')
        return extracted
    start += 1
    for index, item in enumerate(without[start:], start=start):
        if item.content.value <= merge_min:
            break
        # update value of first extraction
        if replace is None:
            extracted[index].content.value = item.content.value
        else:
            extracted[index].content.value = replace
    return extracted
