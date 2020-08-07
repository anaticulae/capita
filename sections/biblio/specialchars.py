# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import texmex

import sections.biblio.utils
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


def analyse_page(navigator: texmex.PageTextNavigator
                ) -> sections.feature.StatisticalResultItem:
    raw = ' '.join([line.text for line in navigator])
    collected = []
    for method in [german.years, german.dates, german.pagenumbers]:
        collected.extend(method(raw))

    marker = len(collected)
    if special_chars(raw):
        # thirty percent bonus
        marker *= 1.3  # TODO: HOLY VALUE

    likelihood = 0.0
    if marker and len(navigator) >= 1:
        likelihood = marker / len(navigator)

    if likelihood < MIN_LIKELIHOOD:
        # TODO: CHECK THIS
        # this can not be a bib table
        marker = 0
    return len(navigator), marker


def special_chars(raw: str) -> list:
    # TODO: A LOT OF MISMATCHES AS A RESULT OF PROGRAM CODE IN DOCUMENT
    result = []
    for line in raw.splitlines():
        parsed = german.split_words(line, validate_sentences=False)
        result.extend(parsed)
    counted = raw.count(';') + raw.count(',') + raw.count('/') + raw.count(':')
    counted += raw.count('[') + raw.count(']') + raw.count(')') + raw.count('(')
    counted += raw.count('&')

    word_count = len(result)
    classifier = counted / word_count if word_count else 0
    if word_count > 40 and classifier > 0.3:  # TODO HOLY VALUE
        return True
    return False
