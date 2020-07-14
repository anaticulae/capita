# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import iamraw


@dataclasses.dataclass
class TableTable(iamraw.AreaItem):
    """Table of table."""


@dataclasses.dataclass
class Abstract(iamraw.AreaItem):
    """Table of table."""


iamraw.sections.TableTable = TableTable
iamraw.sections.Abstract = Abstract
