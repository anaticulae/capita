# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import power
import utila

import sections.feature.abbreviation
import sections.feature.abstract
import sections.feature.acknowledge
import sections.feature.appendix
import sections.feature.bibliography
import sections.feature.chapter
import sections.feature.figuretable
import sections.feature.glossary
import sections.feature.index
import sections.feature.legal
import sections.feature.paper
import sections.feature.section
import sections.feature.symboltable
import sections.feature.tabletable
import sections.feature.title
import sections.feature.toc
import sections.feature.whitepage
import sections.path


def extract_sections_frompath(  # pylint:disable=R0914
    pdf: str,
    prefix: str = '',
    pages: tuple = None,
) -> iamraw.Sections:
    path = power.link(pdf)
    text = iamraw.path.text(path, prefix=prefix)
    textposition = iamraw.path.textposition(path, prefix=prefix)
    toc = iamraw.path.toc(path, prefix=prefix)
    fontheader = iamraw.path.fontheader(path, prefix=prefix)
    fontcontent = iamraw.path.fontcontent(path, prefix=prefix)
    sizeandborder = iamraw.path.sizeandborder(path, prefix=prefix)
    footers = iamraw.path.headerfooters(path, prefix=prefix)
    profile = functools.partial(utila.profile, always=True)
    with profile('abstract'):
        abstract = sections.feature.abstract.work(
            text,
            textposition,
            sizeandborder,
            footers,
            pages=pages,
        )
    with profile('chapter'):
        chapter = sections.feature.chapter.work(
            text,
            textposition,
            sizeandborder,
            footers,
            toc,
            pages=pages,
        )
    with profile('abbreviation'):
        abbreviation = sections.feature.abbreviation.work(
            text,
            textposition,
            pages=pages,
        )
    with profile('appendix'):
        appendix = sections.feature.appendix.work(
            text,
            textposition,
            pages=pages,
        )
    with profile('figuretable'):
        figuretable = sections.feature.figuretable.work(
            text,
            textposition,
            sizeandborder,
            footers,
            pages=pages,
        )
    with profile('bibliography'):
        bibliography = sections.feature.bibliography.work(
            text,
            textposition,
            pages=pages,
        )
    with profile('legal'):
        legal = sections.feature.legal.work(text, textposition, pages=pages)
    with profile('index'):
        index = sections.feature.index.work(
            text,
            textposition,
            sizeandborder,
            footers,
            pages=pages,
        )
    with profile('title'):
        title = sections.feature.title.work(
            text,
            fontheader,
            fontcontent,
            pages=pages,
        )
    with profile('symboltable'):
        symboltable = sections.feature.symboltable.work(
            text,
            textposition,
            pages=pages,
        )
    with profile('tabletable'):
        tabletable = sections.feature.tabletable.work(
            text,
            textposition,
            sizeandborder,
            footers,
            pages=pages,
        )
    with profile('toc'):
        toc = sections.feature.toc.work(
            text,
            textposition,
            sizeandborder,
            footers,
            pages=pages,
        )
    with profile('whitepage'):
        whitepage = sections.feature.whitepage.work(
            text,
            textposition,
            footers=footers,
            pages=pages,
        )
    with profile('acknowledge'):
        acknowledge = sections.feature.acknowledge.work(
            text,
            textposition,
            pages=pages,
        )
    with profile('glossary'):
        glossary = sections.feature.glossary.work(
            text,
            textposition,
            pages=pages,
        )
    with profile('paper'):
        paper = sections.feature.paper.work(
            pdf,
            pages=pages,
        )
    loaded = sections.feature.section.load_features(
        abbreviation,
        abstract,
        acknowledge,
        appendix,
        bibliography,
        chapter,
        figuretable,
        index,
        legal,
        paper,
        symboltable,
        tabletable,
        title,
        toc,
        whitepage,
        xglossary=glossary,
        pages=pages,
    )
    # work
    result = sections.feature.section.extract_sections(loaded)
    return result
