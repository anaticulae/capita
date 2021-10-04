# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
def test_gloassary_work():
    source = power.link(power.DISS143_PDF)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    extracted = sections.feature.glossary.work(
        text,
        textposition,
        pages=None,
    )
    assert len(extracted) > 50, str(extracted)
    loaded = serializeraw.load_likelihood(extracted)
    assert len(loaded) == 4
    pages = [item.page for item in loaded]
    assert pages == [127, 128, 129, 130]
