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
    power.todo(power.MASTER072_PDF),
    power.todo(power.MASTER098_PDF),
    power.todo(power.BACHELOR037_PDF, '0:30'),
    power.todo(power.BACHELOR063_PDF, '0:20,59,60,61'),
    power.todo(power.BACHELOR111_PDF, '0:10,90:111'),
    power.todo(power.BACHELOR056_PDF, '0:55'),
    power.todo(power.MASTER116_PDF, '0:13,85:117'),
    power.todo(power.BACHELOR090_PDF, '0:20,75:90'),
    power.todo(power.DOCU14_PDF),
    power.todo(power.DOCU07_PDF),
    power.todo(power.DOCU09_PDF),
    power.todo(power.DOCU27_PDF),
]

REQURIED_RESOURCES = [power.link(pdf) for pdf, _ in RESOURCES]

REQURIED_RESOURCES = [utila.forward_slash(item) for item in REQURIED_RESOURCES]
