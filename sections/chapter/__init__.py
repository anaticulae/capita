# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import statistics

import configo
import elements.headline.lookup
import iamraw
import texmex
import utila

import sections.chapter.starter

AFTER_HEADER = configo.HV_PERCENT_PLUS(default=5.0)

FIRST_QUARTER = configo.HV_PERCENT_PLUS(default=45.0)

TOCS_COUNT_MIN = configo.HV_INT_PLUS(default=3)


def extract_chapter(
    navigators: texmex.PageTextNavigators,
    tocs,
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
        chapter_rate += rate_fromtoc(tocs, first_content)
        if contains_listof(first_content):
            utila.debug(f'no chapter {page.page}: list of dots')
            # TODO: See todo below
            chapter_rate = 0
        if chapter_rate <= 0.0:
            continue
        rate_in_percent = chaptervalue_to_percent(chapter_rate, tocs)
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


def rate_fromtoc(tocs, pagestart: list) -> float:
    """Try to find potential headline inside toc from outlines.

    If no toc is given, use elements.headlines-list as backup strategy.
    """
    chapter_rate = 0.0
    if len(tocs) >= TOCS_COUNT_MIN:
        chapter_rate = contain_toc(pagestart, tocs)
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


def contains_listof(content: str) -> bool:
    raw = rawcontent(content)
    dots_with_spaces = raw.count('. . . .')
    connected_dots = raw.count('....')
    result = dots_with_spaces > 4 or connected_dots >= 3
    return result


NOHEADLINES = elements.headline.lookup.HEADLINES - elements.headline.lookup.CHAPTER


def contain_toc(content, toc) -> float:
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
                    not startswith(line, headline),
                    not startswith(without_number, headline),
            )):
                continue
            rate = len(without_number) / len(headline)
            if not 0.2 < rate < 2.0:
                # headline is too long or too short, could not match with
                # detected toc
                continue
            return 1.0
    return -0.5


def startswith(line: str, start: str) -> bool:
    """\
    >>> startswith('Methode3', '2 Methode3')
    True
    """
    percent = len(line) / len(start) if line else 0.0
    start = start[0:len(line)]
    maxdiff = 0.9 if len(start) > 10 else 0.7  # TODO: HOLY VALUE
    if percent < 0.5:
        # matched part is to small
        maxdiff = 0.9
    # TODO: REPLACE WITH UTILA CODe
    if utila.similar(start, line, maxdiff=maxdiff):
        return True
    return False


def toc_shrink(items):
    """Remove tocs after Anhang."""
    result = []
    for item in items:
        if 'anhang' in item.lower():
            # TODO: DANGEROUS! ANHANG CAN BE PART OF ANY OTHER HEADLINE
            break
        result.append(item)
    return result


FIRSTLEVEL_DOT_PATTERN = re.compile(r'^\d\.{0,1}\s+')


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


def rawcontent(content) -> str:
    raw = utila.NEWLINE.join([item.text for item in content])
    raw = raw.lower()
    return raw
