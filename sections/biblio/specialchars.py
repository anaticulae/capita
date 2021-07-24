# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Special Chars
=============

Determine potential bib pages dues analysing the structure of used
characters on a page. Bib pages contain a lot of brackets, dots,
semicolons. etc.

A document contains only one bib page(s) block. Therefore we look for
the highest rated valued block of bib pages and return only this single
one. Without selecting the biggest cluster, more than one bib can be
detected.
"""

import statistics

import configo
import german
import texmex
import utila

import sections.biblio.utils
import sections.utils.headline
import sections.utils.spa

MIN_LIKELIHOOD = 0.3  # TODO: HOLY VALUE


def extract(data: sections.utils.spa.Data) -> list:
    config = sections.utils.spa.Config(
        likelihood_name='bibliography_table',
        page_analysis=analyse_page,
    )
    extracted = sections.utils.spa.work(data=data, config=config)
    # ignore to low valued bib pages
    valid = [item for item in extracted if item.content.value > MIN_LIKELIHOOD]
    hugest = sections.biblio.utils.cluster_bibpages(valid)
    return hugest


HEADLINES = [
    'Bibliografie',
    'Bibliographie',
    'Bibliography',
    'Literatur',
    'Literature',
    'Literaturverzeichnis',
    'Quellen',
    'Quellenverzeichnis',
    'Reference',
    'References',
    'Weiterführende Literatur',
]
MARKER_MIN_COUNT = configo.HV_INT_PLUS(5).value


def analyse_page(
    navigator: texmex.PageTextNavigator
) -> sections.feature.StatisticalResultItem:
    headlines = sections.utils.headline.headlines(navigator)
    if headlines and utila.similar(
            expected=HEADLINES,
            current=headlines,
            maxdiff=0.95,
    ):
        # Bibliography headline on page
        return len(navigator), len(navigator)
    raw = ' '.join([line.text for line in navigator])
    pattern = [
        german.dates,
        german.years,
        german.pagenumbers,
        german.authors,
    ]
    collected = collect_and_replace(raw, pattern)
    marker = len(collected)
    if marker < MARKER_MIN_COUNT:
        utila.debug(f'too few marker: {marker}')
        marker = 0

    if special_chars(raw):
        # thirty percent bonus
        marker *= 1.3  # TODO: HOLY VALUE

    if content_page(raw):
        marker = 0

    likelihood = 0.0
    if marker and len(navigator) >= 1:
        likelihood = marker / len(navigator)

    if likelihood < MIN_LIKELIHOOD:
        # TODO: CHECK THIS
        # this can not be a bib table
        marker = 0
    return len(navigator), marker


def collect_and_replace(raw: str, pattern: list) -> list:
    """Collect due list of pattern and avoids parsing items twice."""
    collected = []
    for method in pattern:
        parsed = method(raw, verbose=True)
        for item, itemraw in parsed:
            # do not parse pattern twice
            raw = raw.replace(itemraw, ' **************** ')
            collected.append(item)
    return collected


def special_chars(raw: str) -> bool:
    # TODO: A LOT OF MISMATCHES AS A RESULT OF PROGRAM CODE IN DOCUMENT
    result = []
    for line in raw.splitlines():
        parsed = german.word_tokenize(line, validate_sentences=False)
        result.extend(parsed)
    counted = raw.count(';') + raw.count(',') + raw.count('/') + raw.count(':')
    counted += raw.count('[') + raw.count(']') + raw.count(')') + raw.count('(')
    counted += raw.count('&')

    word_count = len(result)
    classifier = counted / word_count if word_count else 0
    if word_count > 40 and classifier > 0.3:  # TODO HOLY VALUE
        return True
    return False


def content_page(raw: str) -> bool:
    """Verify that page contains a `normal` number of sentences."""
    sentences = german.sentence_tokenize(raw, normalize_spaces=True)
    if not sentences:
        return False
    # german does not split sentences at `:` but bib tables uses : often
    # for separating parts. If we do not split by double collon we archive
    # a lot of false postive results.
    sentences = utila.flatten([item.split(':') for item in sentences])
    length_mean = statistics.mean([len(sentence) for sentence in sentences])
    if length_mean > 100:
        return True
    return False
