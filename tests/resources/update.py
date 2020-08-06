# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import sections

power.setup(sections.ROOT)

RESOURCES = [
    (power.MASTER072_PDF, None),
    (power.MASTER098_PDF, None),
    (power.BACHELOR037_PDF, None),
    (power.BACHELOR063_PDF, '0:20,59,60,61'),
    (power.BACHELOR111_PDF, '0:10,90:111'),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER116_PDF, '0:13,85:117'),
    (power.BACHELOR090_PDF, '0:20,75:90'),
    (power.DOCU14_PDF, None),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.DOCU27_PDF, None),
    (power.DOCU35_PDF, None),
]

REQURIED_RESOURCES = [power.link(pdf) for pdf, _ in RESOURCES]

REQURIED_RESOURCES = [utila.forward_slash(item) for item in REQURIED_RESOURCES]
