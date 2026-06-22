# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import iamraw.path
import serializeraw
import utilo
import utilotest

import capita.feature.legal


def legal(source: str, pages: tuple = None) -> iamraw.PageContentLikelihoods:
    utilotest.fixture_requires(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)

    dumped = capita.feature.legal.work(text, textposition, pages=pages)
    assert dumped, dumped

    loaded = serializeraw.load_likelihood(dumped)
    return loaded


def test_legal_work_master116():
    source = hoverpower.link(hoverpower.MASTER116_PDF)
    pages = (0, 1, 2, 3, 4, 5, 96)

    extracted = legal(source, pages)

    legal_page = utilo.select_page(extracted, page=1)
    assert legal_page.content.value == 1.0, str(extracted)


@utilotest.longrun
def test_legal_work_bachelor63():
    source = hoverpower.link(hoverpower.BACHELOR063_PDF)
    extracted = legal(source)
    legal_page = utilo.select_page(extracted, page=2)
    assert legal_page.content.value == 1.0, str(extracted)
