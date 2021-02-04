# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import power

MASTER = {
    power.MASTER072_PDF: [
        (
            iamraw.sections.Introduction,
            (0, 3),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (3, 65),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (65, 72),
            [],
        ),
    ],
    power.MASTER116_PDF: [
        (
            iamraw.sections.Introduction,
            (0, 8),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (8, 88),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (88, 116),
            [],
        ),
    ],
}
