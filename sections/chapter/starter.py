# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import elements.headline.lookup
import utila

import sections.chapter.utils

HEADLINES_CHECK_FIRST_N_LINES = configo.HV_INT_PLUS(default=4)

NO_CHAPTER_PATTERN_LINE_LENGTH_MAX = configo.HV_INT_PLUS(default=15)

HEADLINE_LENGTH_MAX = configo.HV_INT_PLUS(default=75)

FIRSTLEVEL_CHAPTER_MAX = configo.HV_INT_PLUS(default=13)

HEADLINE_CHARRATE_MIN = configo.HolyTable(items=(
    (0, 0.8),
    (10, 0.75),
    (100, 0.8),
))


def contain_chapter(content) -> float:  # pylint:disable=R1260
    """Check if `content` contains elements which are hints that this
    content is part of the start of the chapter.

    A big hint is that the word `Kapitel` occurs on the start of the
    text. We have to keep in mind, that the sentence: 'Wie in Kapitel ..
    beschrieben' can occurs everywhere, therefore only searching the
    word is not a good approach. Only some documents use this pattern.

    A second option is to look for the headline-pattern: '1. Einleitung'.
    """
    raw = [item.text for item in content[0:HEADLINES_CHECK_FIRST_N_LINES]]
    result = 0.0
    if startwith_chapterpattern(raw):
        result += 0.5
    if startwith_whitelist(raw):
        result += 1.0
    if startwith_firstlevelheadline(raw):
        result += 0.5
    if not result:
        result -= 0.5
    return result


def startwith_chapterpattern(raw: list) -> bool:
    for line in raw:
        # K a p i t e l 1
        nowhitespace = line.replace(' ', '')
        if CHAPTER_PATTERN.match(nowhitespace):
            # KAPITEL 1: EINLEITUNG
            return True
        if 'kapitel' in line or 'chapter' in line:
            if len(line) > NO_CHAPTER_PATTERN_LINE_LENGTH_MAX:
                # skip sentences which contains Chapter or Kapitel
                continue
            return True
    return False


CHAPTER_PATTERN = utila.compiles(r"""
    ^
    (chapter|kapitel)
    [ ]{0,3}
    (1?\d)      # 0-19
    (
        [ ]{0,3}
        \:
        .+
    )?
""")


def startwith_whitelist(raw: list) -> bool:
    for line in raw:
        matched = NUMBER_PATTERN.match(line)
        if not matched:
            continue
        if sections.chapter.utils.huge_match(
                line,
                elements.headline.lookup.CHAPTER,
        ):
            return True
    return False


# We need only one number with dot, because we want only chapters, not
# sections etc.
NUMBER_PATTERN = utila.compiles(r"""
    ^  # page start
    (?P<number>[0-9]{1,2})[\.]{0,1}  # chapter number with dot
    [ ]{1,4}
    [^0-9\n]{5,}  # non numeric element
""")


def startwith_firstlevelheadline(raw: list) -> bool:
    for line in raw:
        matched = NUMBER_PATTERN.match(line)
        if matched:
            line = utila.extract_match(matched)
            if len(line) > HEADLINE_LENGTH_MAX:
                # TODO: REQUIRE A BETTER SELECTOR
                # seam to be a content line.
                continue
            chapternumber = int(matched['number'])
            if chapternumber > FIRSTLEVEL_CHAPTER_MAX:
                utila.debug(f'chapter number to hight: {line}')
                continue
            charrate = utila.char_rate(line)
            charrate_min = HEADLINE_CHARRATE_MIN(len(line))
            if charrate < charrate_min:
                utila.debug(f'char rate to low: {charrate} {line}')
                continue
            return True
    return False


HUGENUMBER_MIN = configo.HV_INT_PLUS(default=25)


def startwith_hugenumber(raw: list) -> bool:
    """There is a chapter start which contain a very large number, the
    headline, and a small toc.

    Example
    -------

    C H A L L E N G E S A N D O V E R V I E W                <huge>3</huge>

    Contents
    3.1 Anomaly detection challenges in distributed software systems .... 28
    3.2 Conceptual overview . . . . . . . . . . . . . . . . . . . . . . . 35

    This chapter describes the main challenges, problems addressed, and as...
    """
    huge = huge_numbers(raw, size_min=HUGENUMBER_MIN)
    if not huge:
        return False
    single = [item for item in raw if utila.issinglechar(item.text)]
    if not single:
        return False
    toc = [
        item for item in raw if utila.verysimilar(
            current=item.text,
            expected=elements.headline.lookup.TOC,
        )
    ]
    if not toc:
        return False
    return True


def huge_numbers(items, size_min: int = 25):
    # TODO: MOVE TO TEXMEX
    result = []
    for item in items:
        for style in item.style:
            if style.size < size_min:
                continue
            text = item.text[style.start:style.end]
            if not utila.isint(text):
                continue
            result.append(int(text))
    return result
