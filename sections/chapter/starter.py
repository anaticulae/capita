# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

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
        result += 1.0
    if startwith_whitelist(raw):
        result += 1.0
    elif startwith_firstlevelheadline(raw):
        result += 0.5
    else:
        result -= 0.5
    return result


def startwith_chapterpattern(raw: list) -> bool:
    for line in raw:
        # K a p i t e l 1
        nowhitespace = line.replace(' ', '')
        if re.match(CHAPTER_PATTERN, nowhitespace):
            # KAPITEL 1: EINLEITUNG
            return True
        if 'kapitel' in line or 'chapter' in line:
            if len(line) > NO_CHAPTER_PATTERN_LINE_LENGTH_MAX:
                # skip sentences which contains Chapter or Kapitel
                continue
            return True
    return False


CHAPTER_PATTERN = re.compile(
    r"""^
    (chapter|kapitel)
    [ ]{0,3}
    (1?\d)      # 0-19
    (
        [ ]{0,3}
        \:
        .+
    )?
""",
    re.VERBOSE,
)


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
