# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import geostrat
import serializeraw
import texmex
import utila

import sections.biblio.utils
import sections.feature
import sections.utils.headline
import sections.utils.spa


def work(document: str, position: str, pages: tuple = None) -> str:
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
    )
    hugest = extract(data)
    dumped = serializeraw.dump_likelihood(hugest)
    return dumped


HEADLINES = utila.splitlines("""
GLOSSAR
GLOSSARY
STICHWORTVERZEICHNIS
""")

MIN_LIKELIHOOD = 0.5  # TODO: HOLY VALUE


def extract(data: sections.utils.spa.Data) -> list:
    config = sections.utils.spa.Config(
        likelihood_name='glossary',
        page_analysis=analyse_page,
    )
    extracted = sections.utils.spa.work(data=data, config=config)
    # ignore to low valued bib pages
    valid = [item for item in extracted if item.content.value > MIN_LIKELIHOOD]
    hugest = sections.biblio.utils.cluster_bibpages(valid)
    return hugest


def analyse_page(
    navigator: texmex.PageTextNavigator
) -> sections.feature.StatisticalResultItem:
    headlines = sections.utils.headline.headlines(navigator)
    if headlines and utila.similar(
            expected=HEADLINES,
            current=headlines,
            maxdiff=0.95,
    ):
        # Gloassray headline on page
        return len(navigator), len(navigator)
    try:
        alternated = geostrat.al_parse_page(navigator)
    except geostrat.AlternateGeometryException:
        # no alternating page content
        return len(navigator), 0
    marker = 0
    for firstline, *content in alternated:
        text = firstline.text.strip()
        if len(text) < 3:
            # skip index pages
            continue
        if len(text.split()) >= 3:
            continue
        if utila.char_rate(text) < 0.9:
            continue
        if len(content) < 3:
            continue
        marker += 5
    if marker < 8:  # TODO: HOLY VALUE
        # min marker
        marker = 0
    return len(navigator), marker
