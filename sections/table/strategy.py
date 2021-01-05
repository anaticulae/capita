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


def work(
        navigators: texmex.PageTextContentNavigators,
        headline: str,
        shortcut: str,
        valid_pages: tuple = None,
        blacklist: list = None,
) -> str:
    extracted = extract_xxx_likelihood(
        navigators,
        headline,
        shortcut=shortcut,
        valid_pages=valid_pages,
        blacklist=blacklist,
    )

    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


NO_PAGE = (0, 0)


def extract_xxx_likelihood(
        document: texmex.PageTextContentNavigators,
        headline: str = None,
        shortcut: str = 'xxx',
        valid_pages: tuple = None,
        blacklist: list = None,
) -> iamraw.PageContentLikelihood:
    """Iterate thru document and determine uni- or multi formed
    likelihood of being a table page."""
    result = {page.page: analyse_page(page) for page in document}

    def valid(item):
        detected = sections.utils.headline.headlines(item, topsearch=True)
        if blacklist and detected in blacklist:
            return False
        if detected and headline:
            if isinstance(headline, str):
                return detected == headline
            return detected in headline
        return False

    result = {
        page: value if ((valid_pages is None or page in valid_pages) and
                        valid(utila.select_page(document, page))) else NO_PAGE
        for page, value in result.items()
    }
    uniformed = sections.feature.uniform_result(result)
    multiformed = sections.feature.multiform_result(result)

    if multiformed is not None:
        uniformed = multiformed
    assert len(uniformed) == len(document)

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, name=shortcut),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result


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
