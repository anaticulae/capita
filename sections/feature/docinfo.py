# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import germania
import iamraw
import serializeraw
import utilo


def work(
    result: str,
    text: str,
    pdfinfo: str = None,
    pages: tuple = None,
) -> str:
    docinfo = serializeraw.create_docinfo(
        sections=result,
        pdfinfo=pdfinfo,
        pages=pages,
    )
    text = serializeraw.load_document(text, pages=pages)
    docinfo.lang = determine_lang(text)
    # dump result
    dumped = serializeraw.dump_docinfo(docinfo)
    return dumped


LANG_PAGES = configos.HV_INT_PLUS(default=20)

LANG_TRUST_MIN = configos.HV_PERCENT_PLUS(default=70)


def determine_lang(text: iamraw.Document) -> iamraw.Language:
    text = text_flat(text)
    lang = germania.lang(text)
    if lang.probability < LANG_TRUST_MIN:
        return iamraw.Language.UNKNOWN
    try:
        return iamraw.Language.from_str(lang.language.name)
    except ValueError:
        return iamraw.Language.UNKNOWN


def text_flat(text: iamraw.Document) -> list:
    pages = utilo.choose_random(text, count=LANG_PAGES, seed=0.5)
    text = [
        [item.text for item in page if len(item.text) > 20] for page in pages
    ]
    text = utilo.flat(text)
    return text
