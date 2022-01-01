# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila

import sections.paper.main


def work(pdf: str, pages=None) -> str:
    if pdf is None:
        utila.error('skip paper, use --pdf to define pdf')
        return '[]'
    utila.exists_assert(pdf)
    detected = sections.paper.main.detect_paper(pdf, pages=pages)
    if detected is None:
        return '[]'
    dumped = dump_groups(detected)
    return dumped


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
