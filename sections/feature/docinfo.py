# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw


def work(result: str, pdfinfo: str = None, pages: tuple = None) -> str:
    docinfo = serializeraw.create_docinfo(
        sections=result,
        pdfinfo=pdfinfo,
        pages=pages,
    )
    dumped = serializeraw.dump_docinfo(docinfo)
    return dumped
