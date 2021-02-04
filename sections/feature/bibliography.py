# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import sections.biblio.strategy
import sections.utils.spa


def work(document: str, position: str, pages: tuple = None) -> str:
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
    )
    hugest = sections.biblio.strategy.extract(data)
    dumped = serializeraw.dump_likelihood(hugest)
    return dumped
