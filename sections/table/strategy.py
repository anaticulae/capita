# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.group
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
        blacklist: list = None,
) -> str:
    extracted = extract_xxx_likelihood(
        navigators,
        headline,
        shortcut=shortcut,
        pages=pages,
        blacklist=blacklist,
    )

    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


def extract_xxx_likelihood(
        document: texmex.PageTextContentNavigators,
        headline: str = None,
        shortcut: str = 'xxx',
        pages: tuple = None,
        blacklist: list = None,
) -> iamraw.PageContentLikelihood:
    """Iterate thru document and determine uni- or multi formed
    likelihood of being a table page."""
    result = {page.page: (page, analyse_page(page)) for page in document}

    result = {
        page: judged if not utila.should_skip(page, pages) and
        matched(content, headline, blacklist) else NO_PAGE
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


def matched(navigator, headline, blacklist) -> bool:
    """Collect headlines from `navigator` and check if given `headline`
    is found and colected headline is not `blacklisted`."""
    detected = sections.utils.headline.headlines(navigator, topsearch=True)
    if blacklist and detected in blacklist:
        return False
    if detected and headline:
        if isinstance(headline, str):
            return detected == headline
        return detected in headline
    return False


def analyse_page(content) -> float:
    """Extract the number of lines which can contain any table-content

    Dots(. . .) are charactaristical for table lines.

    Args:
        page():
    Returns:
        (linecount, possible_table_lines)
    """
    linecount = len(content)
    possible_toc_line = len([line for line in content if valid_line(line.text)])
    # likelihood = possible_toc_line / linecount if linecount else 0.0
    return linecount, possible_toc_line


def valid_line(line: str) -> bool:
    if line.count('. .') > 3:
        return True
    if line.count('..') > 3:
        return True
    if groupme.toc.group.numbered_level(line):
        return True
    return False
