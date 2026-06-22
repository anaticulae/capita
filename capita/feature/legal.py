# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Legal Proclamation Parser
=========================

.. code-block:: none

    Eidesstattliche Erklärung


    Hiermit erkläre ich, dass ich die vorliegende Arbeit selbstständig und
    eigenhändig sowie ohne unerlaubte fremde Hilfe und ausschließlich unter
    Verwendung der aufgeführten Quellen und Hilfsmittel angefertigt habe.


    ------------ --------------
    (Ort, Datum) (Unterschrift)

Special Marks
-------------

Word Groups:

* Eidesstattliche Erklärung
* Selbstständigkeitserklärung
* angefertigt
* aufgeführten Quellen und Hilfsmittel
* ausschließlich
* diese Arbeit
* eigenhändig
* erkläre ich
* fremden Quellen wörtlich
* gleicher oder ähnlicher Form
* hiermit erkläre ich
* selbstständig
* sinngemäß entnommen
* versichere ich
* vorliegende Arbeit

Notes:

* Ort
* Datum
* Unterschrift

Requirements
------------

* do not add to page count
* do not add to table of content

[Theisen]
"""

import configos
import serializeraw
import texmex
import utilo

import capita.utils.spa

FEATURE_POINT_COUNT_MIN = configos.HV_INT_PLUS(default=5)


def work(document: str, position: str, pages=None) -> str:
    data = capita.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
    )

    config = capita.utils.spa.Config(
        likelihood_name='legal',
        page_analysis=analyse_page,
    )

    extracted = capita.utils.spa.work(
        data=data,
        config=config,
    )

    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


def analyse_page(ptn: texmex.PTN) -> capita.feature.StatisticalResultItem:
    raw = ptn.debug
    lower = raw.lower()
    located = [item for item in FEATURE_POINTS if item in lower]
    trust = 0.0
    if 'Eidesstattliche Erklärung' in raw:
        trust += 0.5
    if 'Selbstständigkeitserklärung' in raw:
        trust += 0.5
    feature_point_count = len(located)
    if feature_point_count >= FEATURE_POINT_COUNT_MIN:
        trust += 0.25
    if feature_point_count > 8:
        trust += 0.5
    if feature_point_count < FEATURE_POINT_COUNT_MIN:
        feature_point_count = 0
        trust = 0.0
    return len(located), trust


FEATURE_POINTS = utilo.splitlines("""\
ANGEFERTIGT
ARBEIT
AUFGEFÜHRTEN QUELLEN UND HILFSMITTEL
AUSSCHLIESSLICH
BERICHTE
BÜCHER
DATUM
DIESE ARBEIT
EIDES STATT
EIDESSTATTLICHE ERKLÄRUNG
EIGENHÄNDIG
ENTNOMMEN
ERKLÄRE ICH
FREMDEN QUELLEN WÖRTLICH
GLEICHER ODER ÄHNLICHER FORM
HIERMIT ERKLÄRE ICH
HILFSMITTEL
INTERNETSEITEN
KEINER ANDEREN PRÜFUNGSKOMMISSION VORGELEGT
KENNTLICH GEMACHT
NICHT VERÖFFENTLICHT
ORT
PRÜFUNGSLEISTUNG
QUELLEN
SELBSTSTÄNDIG
SELBSTSTÄNDIGKEITSERKLÄRUNG
SINNGEMÄSS
SINNGEMÄSS ENTNOMMEN
STUDIENLEISTUNG
UNTERSCHRIFT
VERFASST WORDEN IST
VERSICHERE ICH
VORLIEGENDE ARBEIT
WÖRTLICH
ZITATE AUS FREMDEN ARBEITEN
ÄHNLICHER FORM
""")
