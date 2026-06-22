# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Add experimental code here."""

import iamraw


def simple_content(items: iamraw.PageContentLikelihoods):
    assert isinstance(items, list), type(items)
    result = [item.content.value for item in items]
    return result
