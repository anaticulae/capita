# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw.path
import pytest
import serializeraw
import utilo
import utilotest

import sections.feature.glossary


@utilotest.longrun
@utilotest.requires(hoverpower.DISS143_PDF)
def test_glossary_work_diss143():
    pages = glossary(hoverpower.DISS143_PDF)
    assert pages == [127, 128, 129, 130]


@utilotest.nightly
@pytest.mark.parametrize('source, pages', [
    pytest.param(hoverpower.BACHELOR076_PDF, None, id='bachelor076'),
    pytest.param(hoverpower.BOOK173_PDF, None, id='book173'),
    pytest.param(hoverpower.DISS173_PDF, utilo.rtuple(50), id='diss173'),
    pytest.param(hoverpower.DISS287_PDF, None, id='diss287'),
])
def test_no_glossary_regression_x(source, pages):
    """Do not detect page 142 as glossary. It's just a page about glossaries."""
    utilotest.fixture_requires(source)
    extracted = glossary(source, pages)
    assert not extracted


def glossary(source, pages: tuple = None):
    source = hoverpower.link(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    pdfinfo = iamraw.path.pdfinfo(source)
    extracted = sections.feature.glossary.work(
        text,
        textposition,
        pdfinfo=pdfinfo,
        pages=pages,
    )
    loaded = serializeraw.load_likelihood(extracted)
    pages = [item.page for item in loaded]
    return pages
