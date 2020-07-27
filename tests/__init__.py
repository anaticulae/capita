# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utilatest

import sections
import sections.cli

#pylint:disable=C0103
run_sections = functools.partial(
    utilatest.run_command,
    main=sections.cli.main,
    process=sections.PROCESS,
    success=True,
)

run_sections_failure = functools.partial(
    utilatest.run_command,
    main=sections.cli.main,
    process=sections.PROCESS,
    success=False,
)
