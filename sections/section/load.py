# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import functools

import configo
import iamraw
import serializeraw
import utila


@dataclasses.dataclass
class SectionsRequiredResources:
    abbreviation: iamraw.PageContentLikelihoods
    abstract: iamraw.PageContentLikelihoods
    acknowledge: iamraw.PageContentLikelihoods
    appendix: iamraw.PageContentLikelihoods
    bibliography: iamraw.PageContentLikelihoods
    chapter: iamraw.PageContentLikelihoods
    figuretable: iamraw.PageContentLikelihoods
    index: iamraw.PageContentLikelihoods
    legal: iamraw.PageContentLikelihoods
    paper: iamraw.PageContentLikelihoods
    symboltable: iamraw.PageContentLikelihoods
    tabletable: iamraw.PageContentLikelihoods
    title: iamraw.PageContentLikelihoods
    toc: iamraw.PageContentLikelihoods
    whitepage: list[iamraw.sections.WhitePage]
    glossary: iamraw.PageContentLikelihoods

    def sync(self):
        data = list(vars(self).values())
        for pagenumber, content in utila.sync_pages(iterators=data):
            yield pagenumber, content


@functools.lru_cache(configo.CACHE_SMALL)
def load_features(  # pylint:disable=R0913,R0914
    xabbreviation: str,
    xabstract: str,
    xacknowledge: str,
    xappendix: str,
    xbibliography: str,
    xchapter: str,
    xfiguretable: str,
    xindex: str,
    xlegal: str,
    xpaper: str,
    xsymboltable: str,
    xtabletable: str,
    xtitle: str,
    xtoc: str,
    xwhitepage: str,
    xglossary: str,
    pages: tuple = None,
) -> SectionsRequiredResources:
    abbreviation = serializeraw.load_likelihood(xabbreviation, pages=pages)
    abstract = serializeraw.load_likelihood(xabstract, pages=pages)
    appendix = serializeraw.load_likelihood(xappendix, pages=pages)
    acknowledge = serializeraw.load_likelihood(xacknowledge, pages=pages)
    bibliography = serializeraw.load_likelihood(xbibliography, pages=pages)
    chapter = serializeraw.load_likelihood(xchapter, pages=pages)
    figuretable = serializeraw.load_likelihood(xfiguretable, pages=pages)
    index = serializeraw.load_likelihood(xindex, pages=pages)
    legal = serializeraw.load_likelihood(xlegal, pages=pages)
    paper = serializeraw.load_likelihood(xpaper, pages=pages)
    symboltable = serializeraw.load_likelihood(xsymboltable, pages=pages)
    tabletable = serializeraw.load_likelihood(xtabletable, pages=pages)
    title = serializeraw.load_likelihood(xtitle, pages=pages)
    toc = serializeraw.load_likelihood(xtoc, pages=pages)
    white = serializeraw.load_whitepages(xwhitepage, pages=pages)
    glossary = serializeraw.load_likelihood(xglossary, pages=pages)
    # prepare result
    result = SectionsRequiredResources(
        abbreviation=abbreviation,
        abstract=abstract,
        acknowledge=acknowledge,
        appendix=appendix,
        bibliography=bibliography,
        chapter=chapter,
        figuretable=figuretable,
        index=index,
        legal=legal,
        paper=paper,
        symboltable=symboltable,
        tabletable=tabletable,
        title=title,
        toc=toc,
        whitepage=white,
        glossary=glossary,
    )
    return result
