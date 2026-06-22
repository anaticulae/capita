# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita.feature.index
import capita.strategy
import hoverpower
import iamraw.path
import serializeraw
import utilo
import utilotest

# manually set to secure index finder quality, TODO: investigate later
LAST_PAGE_INDEX_LIKELYHOOD = 0.45


@utilotest.longrun
@utilotest.requires(hoverpower.DOCU027_PDF)
def test_extract_index_likelihood():
    result = index(hoverpower.DOCU027_PDF)
    result = [item.content.value for item in result]
    assert 0.95 <= sum(result) <= 1.05
    # The index is on the last page
    last_page = result[-1]
    assert last_page >= LAST_PAGE_INDEX_LIKELYHOOD, result


@utilotest.longrun
@utilotest.requires(hoverpower.DOCU027_PDF)
def test_index_work():
    result = index(hoverpower.DOCU027_PDF)
    dumped = serializeraw.dump_likelihood(result)
    assert len(dumped) > 100


@utilotest.longrun
@utilotest.requires(hoverpower.DOCU014_PDF)
def test_regression_extract_index_likelihood():
    """Reduce false detection of index-pages"""
    result = index(hoverpower.DOCU014_PDF)
    # lower than five percent
    lower_than_five_percent = [item.content.value < 0.05 for item in result]
    assert all(lower_than_five_percent), lower_than_five_percent


@utilotest.longrun
@utilotest.requires(hoverpower.BOOK173_PDF)
def test_index_book173():
    loaded = index(
        hoverpower.BOOK173_PDF,
        pages=utilo.rtuple(150, 174),
    )
    expected = [164, 165, 166, 167, 168, 169, 170, 171, 172]
    pages = [item.page for item in loaded if item.content.value > 0.4]
    assert pages == expected


def index(source, pages: tuple = None, prefix: str = 'oneline'):
    source = hoverpower.link(source)
    dumped = capita.feature.index.work(
        iamraw.path.text(source, prefix=prefix),
        iamraw.path.textposition(source, prefix=prefix),
        iamraw.path.sizeandborder(source),
        iamraw.path.groupme_headerfooters(source),
        pages=pages,
    )
    loaded = serializeraw.load_likelihood(dumped)
    return loaded
