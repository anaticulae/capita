# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Glossary Section Detector
=========================

Stichwortverzeichnis

Ausfall

    Entspricht ein System nicht mehr den an es gestellten Anforderungen,
    so ist es nicht mehr funktionstüchtig, ausgefallen.

Ausfallkriterium

    Ein Ausfallkriterium beschreibt die messtechnisch erfassbare Schwelle,
    die deﬁnitionsgemäß zwei Zustände eines zu überwachenden Systems trennt.
    Meist ist der Zustand jenseits erreichten Ausfallkriteriums ein Bereich,
    in dem das System den an es gestellten Anforderungen nicht mehr entspricht
    und damit als ausgefallen angesehen werden kann.
"""

import configo
import elements
import geostrat
import serializeraw
import texmex
import utila

import sections.biblio.utils
import sections.feature
import sections.utils.headline
import sections.utils.spa


def work(
    document: str,
    position: str,
    pdfinfo: str,
    pages: tuple = None,
) -> str:
    page_count = 256
    if utila.exists(pdfinfo):
        page_count = serializeraw.load_pdfinfo(pdfinfo).pages
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
        page_count=page_count,
    )
    hugest = extract(data)
    dumped = serializeraw.dump_likelihood(hugest)
    return dumped


LIKELIHOOD_MIN = configo.HolyTable(
    items=[
        (0.0, 0.5),
        (0.2, 0.5),
        (0.25, 0.9),
        (0.65, 0.9),
        (0.75, 0.5),
        (1.0, 0.5),
    ],
    strategy=utila.Strategy.LINEARISE,
)

MARKER_COUNT_MIN = configo.HolyTable(items=[
    (0, 5),
    (6, 5),
    (10, 8),
    (15, 12),
    (20, 14),
    (30, 22),
    (35, 23),
])


def extract(data: sections.utils.spa.Data) -> list:
    config = sections.utils.spa.Config(
        likelihood_name='glossary',
        page_analysis=analyse_page,
    )
    extracted = sections.utils.spa.work(data=data, config=config)
    # ignore to low valued glossary pages
    valid = [
        item for item in extracted
        if item.content.value > LIKELIHOOD_MIN(item.page / data.page_count)
    ]
    hugest = sections.biblio.utils.cluster_bibpages(
        valid,
        likelihood_name='glossary',
    )
    return hugest


LINES_PER_PAGE_MAX = configo.HV_INT_PLUS(default=45)


def analyse_page(
    navigator: texmex.PTN,
    page_count: int,
) -> sections.feature.StatisticalResultItem:
    if not navigator:
        # empty page
        return 0, 0
    if len(navigator) > LINES_PER_PAGE_MAX:
        # too many lines, may a table, figure or something page
        return len(navigator), 0
    headlines = sections.utils.headline.headlines(navigator)
    with_headline = headlines and utila.similar(
        expected=elements.GLOSSARY,
        current=headlines,
        maxdiff=0.95,
    )
    try:
        alternated = geostrat.al_parse_page(navigator)
    except geostrat.AlternateGeometryException:
        # no alternating page content
        return len(navigator), 0
    marker = 0
    for firstline, *content in alternated:
        if no_glossary(firstline, content):
            continue
        marker += 1 + len(content)
    marker_count_min = MARKER_COUNT_MIN(len(navigator))
    if marker < marker_count_min:
        # min marker
        marker = 0
    if marker and with_headline:
        # Glossary headline on page
        return len(navigator), len(navigator)
    # limit marker without headline to avoid glossaries inside document
    rate_required = LIKELIHOOD_MIN(navigator.page / page_count)
    rate = marker / len(navigator)
    if rate < rate_required:
        return len(navigator), 0
    return len(navigator), marker


def no_glossary(left, content) -> bool:
    text = left.text.strip()
    if len(text) < 3:
        # skip index pages
        return True
    if len(text.split()) >= 3:
        return True
    if utila.char_rate(text) < 0.9:
        return True
    if len(content) < 3:
        return True
    return False
