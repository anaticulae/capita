# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw
import utilatest

import sections.feature.glossary


@utilatest.requires(power.DISS143_PDF)
def test_glossary_work_diss143():
    pages = glossary(power.DISS143_PDF)
    assert pages == [127, 128, 129, 130]


@utilatest.nightly
@utilatest.requires(power.BOOK173_PDF)
def test_glossary_work_book173():
    """Do not detect page 142 as glossary. It's just a page about glossaries."""
    pages = glossary(power.power.BOOK173_PDF)
    assert not pages


def glossary(source, pages: tuple = None):
    source = power.link(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    extracted = sections.feature.glossary.work(
        text,
        textposition,
        pages=None,
    )
    loaded = serializeraw.load_likelihood(extracted)
    pages = [item.page for item in loaded]
    return pages
