# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import serializeraw
import utila

import pdfinfo.pages
import sections.paper.main

PAGES_MIN = configo.HV_INT_PLUS(default=120)


def work(pdf: str, pages=None) -> str:
    if pdf is None:
        utila.error('skip paper, use --pdf to define pdf')
        return NOPAPER
    utila.exists_assert(pdf)
    if skip_strategy(pdf):
        return NOPAPER

    detected = sections.paper.main.detect_paper(pdf, pages=pages)
    if detected is None:
        return NOPAPER
    dumped = dump_groups(detected)
    return dumped


def skip_strategy(pdf: str) -> bool:
    # TODO: USE DOCTYPE ALSO
    pages_max = pdfinfo.pages.determine(pdf)
    if pages_max < PAGES_MIN:
        utila.debug(f'do not search papers, document too short: {pages_max}')
        return True
    return False


NOPAPER = '[]'


def dump_groups(grouped) -> str:
    collected = []
    for group in grouped:
        for page in range(group[0], group[-1] + 1):
            collected.append(
                iamraw.PageContentLikelihood(
                    page=page,
                    content=iamraw.Likelihood(name='paper', value=1.0),
                ))
    result = serializeraw.dump_likelihood(collected)
    return result
