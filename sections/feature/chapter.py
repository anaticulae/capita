# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
* TODO: REQUIRE APPROACH FOR SHORT PAPERS WIHTOUT CHPATER START AT TOP OF PAGE
"""

import re

import iamraw
import serializeraw
import texmex
import utila


def work(
    document: str,
    position: str,
    sizeandborder: str,
    footerheader: str,
    tocpath: str,
    pages: tuple = None,
) -> str:
    """Determine likelihood of beeing a chapter startpage."""
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=document,
        textpositions=position,
        sizeandborderpath=sizeandborder,
        headerfooterpath=footerheader,
        pages=pages,
    )
    tocs = load_toc(tocpath)
    # work
    result = extract_chapter(
        navigators=navigators,
        tocs=tocs,
    )
    # write result
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def load_toc(tocpath):
    """Load table of content out of outlines.

    Strip first outline wich is may the headline of the document.
    """
    toc = serializeraw.load_toc(tocpath)
    if len(toc) == 1:
        # maybe a headline
        toc: iamraw.Toc = iamraw.Toc(children=toc[0].children)
    return toc


AFTER_HEADER = 0.05  # TODO: HOLY VALUE
FIRST_QUARTER = 0.35  # TODO: HOLY VALUE


def extract_chapter(
    navigators: texmex.PageTextNavigators,
    tocs,
) -> iamraw.PageContentLikelihoods:
    result = []
    for page in navigators:
        if rotated(page):
            continue
        first_content = page.between(AFTER_HEADER, FIRST_QUARTER)
        chapter_rate = contain_chapter(first_content)
        if len(tocs) >= 3:  # TODO: HOLY VALUE
            chapter_rate += contain_toc(first_content, tocs)
        else:
            # disable feature if no toc is given
            utila.info('chapter: no toc provided')
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


CHAPTER_PATTERN = re.compile(
    r"""^
    (chapter|kapitel)
    [ ]{0,3}
    \d{1,2}
    [ ]{0,3}
    \:
    .+
""",
    re.VERBOSE,
)

# We need only one number with dot, because we want only chapters, not
# sections etc.
NUMBER_PATTERN = re.compile(
    r'^'  # page start
    r'(?P<number>[0-9]{1,2})[\.]{0,1}'  # chapter number with dot
    r'[ ]{1,4}'
    r'[^0-9\n]{5,}',  # non numeric element
    re.VERBOSE,
)

HEADLINES_CHECK_FIRST_N_LINES = 4
HEADLINE_LENGTH_MAX = 75


def contain_chapter(content) -> float:  # pylint:disable=R1260
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
            if re.match(CHAPTER_PATTERN, line):
                # KAPITEL 1: EINLEITUNG
                return True
            if 'kapitel' in line or 'chapter' in line:
                if len(line) > 15:  # TODO: HOLY VALUE
                    # skip sentences which contains Chapter or Kapitel
                    continue
                return True
        return False

    def startwith_firstlevelheadline(raw: list) -> bool:
        raw = [item.text for item in raw[0:HEADLINES_CHECK_FIRST_N_LINES]]
        for line in raw:
            matched = re.match(NUMBER_PATTERN, line)
            if matched:
                line = utila.extract_match(matched)
                if len(line) > HEADLINE_LENGTH_MAX:
                    # TODO: REQUIRE A BETTER SELECTOR
                    # seam to be a content line.
                    continue
                chapternumber = int(matched['number'])
                if chapternumber > 13:  # TODO: HOLY VALYE
                    utila.debug(f'chapter number to hight: {line}')
                    continue
                return True
        return False

    def startwith_whitelist(raw: list) -> bool:
        raw = [item.text for item in raw[0:HEADLINES_CHECK_FIRST_N_LINES]]
        for line in raw:
            matched = re.match(NUMBER_PATTERN, line)
            if not matched:
                continue
            if any(huge_match(line, item) for item in HEADLINES_CHAPTER):
                return True
        return False

    result = 0.0
    if startwith_chapterpattern(content):
        result += 1.0
    if startwith_whitelist(content):
        result += 1.0
    elif startwith_firstlevelheadline(content):
        result += 0.5
    else:
        result -= 0.5
    return result


def huge_match(line: str, part: str) -> bool:
    """Ensure that matched `part` is long enough in detected line.

    >>> huge_match('20 Bilanz und Ausblick einer Wissenschaft', 'Ausblick')
    False
    """
    line = line.lower()
    if part not in line:
        return False
    percent = len(part) / len(line)
    if percent < 0.5:
        # matched part is to small
        return False
    return True


def contains_listof(content: str) -> bool:
    raw = rawcontent(content)
    dots_with_spaces = raw.count('. . . .')
    connected_dots = raw.count('....')
    result = dots_with_spaces > 4 or connected_dots >= 3
    return result


NOHEADLINES = utila.splitlines("""
ABBILDUNGSVERZEICHNIS
ABKÜRZUNGSVERZEICHNIS
ABSTRACT
ABSTRACT OF THE DISSERTATION
ACKNOWLEDGMENTS
ANHANG
CURRICULUM VITAE
DANKSAGUNG
DEDICATION
EIDESSTATTLICHE ERKLÄRUNG
INHALTSVERZEICHNIS
LIST OF FIGURES
LIST OF TABLES
PUBLICATIONS
REFERENCES
SYMBOLVERZEICHNIS
TABELLENVERZEICHNIS
TABLE OF CONTENTS
VORWORT
ZUSAMMENFASSUNG
""")

HEADLINES_CHAPTER = utila.splitlines("""
AUSBLICK
DISKUSSION
DISKUSSION UND AUSBLICK
EINLEITUNG
EINLEITUNG UND ZIELSETZUNG
ERGEBNISSE
GRUNDLAGEN
INTRODUCTION
SCHLUSSBETRACHTUNG
STAND DES WISSENS
""")


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


def startswith(line, start):
    start = start[0:len(line)]
    return line.startswith(start)


def toc_shrink(items):
    """Remove tocs after Anhang."""
    result = []
    for item in items:
        if 'anhang' in item.lower():
            break
        result.append(item)
    return result


FIRSTLEVEL_DOT_PATTERN = re.compile(r'^\d\.{0,1}\s+')


def level_remove(toc):
    flat = [FIRSTLEVEL_DOT_PATTERN.sub('', item.title) for item in toc]
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


def rotated(navigator) -> bool:
    if not navigator:
        # empty page
        return False
    return navigator.width > navigator.height
