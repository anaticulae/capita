# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections

# yapf:disable
EXAMPLE = [
    iamraw.sections.Introduction(start=0, end=0, trust=1.0, content=[
            iamraw.sections.TitlePage(start=0, end=0, trust=0.98)
        ],
    ),
    iamraw.sections.Table(start=1, end=2, trust=1.0, content=[
            iamraw.sections.TableOfContent(start=1, end=1, trust=0.81),
            iamraw.sections.TableOfContent(start=2, end=2, trust=0.9)
        ],
    ),
    iamraw.sections.MainPart(start=3, end=9, trust=1.0, content=[
            iamraw.sections.Chapter(start=3, end=3, trust=0.5, number=1, title='Kapitel 1'),
            iamraw.sections.Text(start=4, end=4, trust=1.0),
            iamraw.sections.Text(start=5, end=5, trust=1.0),
            iamraw.sections.Chapter(start=6, end=6, trust=0.5, number=2, title='Kapitel 2'),
            iamraw.sections.Text(start=7, end=7, trust=1.0),
            iamraw.sections.Text(start=8, end=8, trust=1.0),
            iamraw.sections.Text(start=9, end=9, trust=1.0)
        ],
    ),
    iamraw.sections.Appendix(start=10, end=12, trust=1.0, content=[
            iamraw.sections.Bibliography(start=10, end=10, trust=0.9),
            iamraw.sections.Bibliography(start=11, end=11, trust=0.86),
            iamraw.sections.LegalInformation(start=12, end=12, trust=1.0)
        ],
    ),
]
# yapf:enable
