# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw
import utila
import utilatest

import sections.feature.index
import sections.table.strategy

# manually set to secure index finder quality, TODO: investigate later
LAST_PAGE_INDEX_LIKELYHOOD = 0.45


@utilatest.requires(power.DOCU027_PDF)
def test_extract_index_likelihood():
    result = index(power.DOCU027_PDF)
    result = [item.content.value for item in result]
    assert 0.95 <= sum(result) <= 1.05
    # The index is on the last page
    last_page = result[-1]
    assert last_page >= LAST_PAGE_INDEX_LIKELYHOOD, result


@utilatest.requires(power.DOCU027_PDF)
def test_index_work():
    result = index(power.DOCU027_PDF)
    dumped = serializeraw.dump_likelihood(result)
    assert len(dumped) > 100


@utilatest.requires(power.DOCU014_PDF)
def test_feature_index_extract_index_likelihood():
    """Reduce false detection of index-pages"""
    result = index(power.DOCU014_PDF)
    # lower than five percent
    lower_than_five_percent = [item.content.value < 0.05 for item in result]
    assert all(lower_than_five_percent), lower_than_five_percent


@utilatest.requires(power.BOOK173_PDF)
def test_index_work_book173():
    loaded = index(
        power.BOOK173_PDF,
        pages=utila.rtuple(150, 174),
    )
    expected = [164, 165, 166, 167, 168, 169, 170, 171, 172]
    pages = [item.page for item in loaded if item.content.value > 0.4]
    assert pages == expected


def index(source, pages: tuple = None, prefix: str = 'oneline'):
    source = power.link(source)
    dumped = sections.feature.index.work(
        iamraw.path.text(source, prefix=prefix),
        iamraw.path.textposition(source, prefix=prefix),
        iamraw.path.sizeandborder(source),
        iamraw.path.groupme_headerfooters(source),
        pages=pages,
    )
    loaded = serializeraw.load_likelihood(dumped)
    return loaded
