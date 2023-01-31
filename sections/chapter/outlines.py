# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Chapter: Outlines
=================

Try to find text on the page which matches with lines from the outlines.

In most cases, if outlines are given, there represent the headlines
inside the document.
"""

import re

import configo
import elements.headline.lookup
import utila

import sections.chapter.utils

TOCS_COUNT_MIN = configo.HV_INT_PLUS(default=3)


def rate_from_outlines(tocs, pagestart: list) -> float:
    """Try to find potential headline inside toc from outlines.

    If no toc is given, use elements.headlines-list as backup strategy.
    """
    chapter_rate = 0.0
    if len(tocs) >= TOCS_COUNT_MIN:
        chapter_rate = contains_outline(pagestart, tocs)
        return chapter_rate
    # disable feature if no toc is given
    utila.info('chapter: no toc provided')
    # try backup
    matched = any(
        utila.similar(
            expected=HEADLINES_BACKUP,
            current=item.text,
            maxdiff=0.9,
        ) for item in pagestart)
    if matched:
        return 1.0
    return 0.0


HEADLINES_BACKUP = elements.headline.lookup.CHAPTER


def contains_outline(content, toc) -> float:
    """Check that content starts with a parsed headline entree.

    Supported Pattern; line starts with:
        * 3. Headline text
        * Headline text
    """
    flat_toc = level_remove(toc)
    flat_toc = toc_shrink(flat_toc)
    if not flat_toc:
        # no table of content was extracted
        return 0.0
    flat_toc = [item for item in flat_toc if item.lower() not in NOHEADLINES]
    for line in content:
        line = utila.normalize_whitespaces(line.text.strip())
        if utila.issinglechar(line):
            # I N T R O D U C T I O N 1
            line = line.replace(' ', '')
        # remove numbered headline pattern and potential white spaces
        without_number = FIRSTLEVEL_DOT_PATTERN.sub('', line)
        for headline in flat_toc:
            if all((
                    not sections.chapter.utils.startswith(line, headline),
                    not sections.chapter.utils.startswith(
                        without_number, headline),
            )):
                continue
            rate = len(without_number) / len(headline)
            if not 0.2 < rate < 2.0:
                # headline is too long or too short, could not match with
                # detected toc
                continue
            return 1.0
    return -0.5


NOHEADLINES = elements.headline.lookup.HEADLINES - elements.headline.lookup.CHAPTER

FIRSTLEVEL_DOT_PATTERN = re.compile(r'^\d{1,2}\.{0,1}\s+')


def level_remove(toc):
    flat = []
    for item in toc:
        if not item.title.strip():
            # invalid outlines can break further processing
            utila.debug('empty outline element')
            continue
        flat.append(FIRSTLEVEL_DOT_PATTERN.sub('', item.title))
    # remove roman level
    result = []
    for item in flat:
        splitted = item.split(maxsplit=1)
        if len(splitted) == 1:
            result.append(item)
            continue
        if utila.isroman(splitted[0]):
            result.append(splitted[1])
            continue
        result.append(item)
    return result


def toc_shrink(items):
    """Remove tocs after Anhang."""
    result = []
    for item in items:
        if 'anhang' in item.lower():
            # TODO: DANGEROUS! ANHANG CAN BE PART OF ANY OTHER HEADLINE
            break
        result.append(item)
    return result
