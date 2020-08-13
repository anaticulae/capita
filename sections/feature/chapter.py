# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Chapter Start Determination
===========================

Find the starts of a chapter.

What is typical for a start of chapter?

* Mostly there is a space between header and title start
* There is a number/chapter number
* There is a huge font
* The title is listed in table of content


1. Locate the distance between first line and header
2. Check the second line

QUESTIONS:

* TODO: Are chapters only content based or is appendix etc. a chapter too?
"""

import re

import iamraw
import serializeraw
import texmex
import utila


def work(
        document: str,
        position: str,
        tocpath: str,
        pages: tuple = None,
) -> str:
    """Determine likelihood of beeing a chapter startpage."""
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text=document,
        textpositions=position,
        pages=pages,
    )
    tocs = serializeraw.load_toc(tocpath)

    # work
    result = extract_chapter(
        navigators=navigators,
        tocs=tocs,
    )

    # write result
    dumped = serializeraw.dump_likelihood(result)
    return dumped


AFTER_HEADER = 0.05  # TODO: HOLY VALUE
FIRST_QUARTER = 0.35  # TODO: HOLY VALUE


def extract_chapter(
        navigators: texmex.PageTextNavigators,
        tocs,
) -> iamraw.PageContentLikelihoods:
    result = []
    for page in navigators:
        first_content = page.between(AFTER_HEADER, FIRST_QUARTER)

        chapter_rate = contain_chapter(first_content)
        chapter_rate += contain_toc(first_content, tocs)

        if contains_listof(first_content):
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


# We need only one number with dot, because we want only chapters, not
# sections etc.
NUMBER_PATTERN = re.compile(
    r'^'  # page start
    r'[0-9]{1,2}[\.]{0,1}'  # chapter number with dot
    r'[ ]{1,4}'
    r'[^0-9\n]{5,}',  # non numeric element
    re.VERBOSE,
)

HEADLINES_CHECK_FIRST_N_LINES = 4


def contain_chapter(content) -> float:
    """Check if `content` contains elements which are hints that this
    content is part of the start of the chapter.

    A big hint is that the word `Kapitel` occurs on the start of the
    text. We have to keep in mind, that the sentence: 'Wie in Kapitel ..
    beschrieben' can occurs everywhere, therefore only searching the
    word is not a good approach. Only some documents use this pattern.

    A second option is to look for the headline-pattern: '1. Einleitung'.
    """

    def startwith_chapterpattern(raw: list) -> bool:
        raw = [
            item.text.lower() for item in raw[0:HEADLINES_CHECK_FIRST_N_LINES]
        ]
        for line in raw:
            if 'kapitel' in line or 'chapter' in line:
                return True
        return False

    def startwith_firstlevelheadline(raw: list) -> bool:
        raw = [item.text for item in raw[0:HEADLINES_CHECK_FIRST_N_LINES]]
        for line in raw:
            matched = re.match(NUMBER_PATTERN, line)
            if matched:
                return True
        return False

    result = 0.0
    if startwith_chapterpattern(content):
        result += 1.0
    if startwith_firstlevelheadline(content):
        result += 0.5
    else:
        result -= 0.5
    return result


def contains_listof(content: str) -> bool:
    raw = rawcontent(content)
    dots_with_spaces = raw.count('. . . .')
    connected_dots = raw.count('....')

    result = dots_with_spaces > 4 or connected_dots >= 3
    return result


BLACKLIST = {
    'Abbildungsverzeichnis',
    'Abkürzungsverzeichnis',
    'Inhaltsverzeichnis',
    # 'Literaturverzeichnis',
    'Tabellenverzeichnis',
    'Vorwort',
}


def contain_toc(content, toc) -> float:
    """Check that content starts with a parsed headline entree.

    Supported Pattern; line starts with:
        * 3. Headline text
        * Headline text
    """
    firstlevel_dot_pattern = re.compile(r'^\d\.{0,1}\s+')

    flat_toc = [firstlevel_dot_pattern.sub('', item.title) for item in toc]
    if not flat_toc:
        # no table of content was extracted
        return 0.0

    flat_toc = [item for item in flat_toc if item not in BLACKLIST]

    for line in content:
        line = line.text.strip()
        # remove numbered headline pattern and potential white spaces
        without_number = firstlevel_dot_pattern.sub('', line)
        for headline in flat_toc:
            if all((
                    not line.startswith(headline),
                    not without_number.startswith(headline),
            )):
                continue
            return 1.0
    return -0.5


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
