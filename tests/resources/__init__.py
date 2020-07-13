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

# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
HOWTO_PYPORTING_CHAPTER_PAGE_COUNT = 2

power.setup(sections.ROOT)

REQURIED_RESOURCES = [
    power.link(power.MASTER072_PDF),
    power.link(power.MASTER098_PDF),
    power.link(power.BACHELOR037_PDF),
    power.link(power.BACHELOR063_PDF),
    power.link(power.BACHELOR111_PDF),
    power.link(power.BACHELOR056_PDF),
    power.link(power.MASTER116_PDF),
    power.link(power.DOCU14_PDF),
    power.link(power.DOCU07_PDF),
    power.link(power.DOCU09_PDF),
    power.link(power.DOCU27_PDF),
]

REQURIED_RESOURCES = [utila.forward_slash(item) for item in REQURIED_RESOURCES]
