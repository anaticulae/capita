# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections
import power

BACHELOR = {
    power.BACHELOR037_PDF: [
        (
            iamraw.sections.Introduction,
            (0, 6),
            [
                (iamraw.sections.TitlePage, (0, 1)),
                (iamraw.sections.AbbreviationTable, (1, 2)),
                (iamraw.sections.FigureTable, (2, 3)),
                (iamraw.sections.TableOfContent, (3, 5)),
                (iamraw.sections.Unknown, (5, 6)),  # TODO: ABSTRACT
            ],
        ),
        (
            iamraw.sections.MainPart,
            (6, 33),
            [
                (iamraw.sections.Chapter, (7, 8)),
                (iamraw.sections.Text, (8, 15)),
                (iamraw.sections.Chapter, (15, 16)),
                (iamraw.sections.Text, (16, 22)),
                (iamraw.sections.Chapter, (22, 23)),
                (iamraw.sections.Text, (23, 27)),
                (iamraw.sections.Chapter, (27, 28)),
                (iamraw.sections.Text, (28, 33)),
            ],
        ),
        (
            iamraw.sections.Appendix,
            (33, 37),
            [
                (iamraw.sections.Bibliography, (33, 37)),
            ],
        ),
    ],
    power.BACHELOR056_PDF: [
        (
            iamraw.sections.Introduction,
            (0, 5),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (0, 5),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (50, 56),
            [],
        ),
    ],
    power.BACHELOR063_PDF: [
        (
            iamraw.sections.Introduction,
            (0, 8),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (8, 43),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (43, 63),
            [],
        ),
    ],
    power.BACHELOR090_PDF: [
        (
            iamraw.sections.Unknown,
            (0, 1),
            [],
        ),
        (
            iamraw.sections.Introduction,
            (1, 12),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (12, 76),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (76, 90),
            [],
        ),
    ],
    power.BACHELOR111_PDF: [
        (
            iamraw.sections.Introduction,
            (0, 5),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (5, 84),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (84, 111),
            [],
        ),
    ],
    power.BACHELOR090_PDF: [
        (
            iamraw.sections.Unknown,
            (0, 1),
            [],
        ),
        (
            iamraw.sections.Introduction,
            (1, 12),
            [],
        ),
        (
            iamraw.sections.MainPart,
            (12, 76),
            [],
        ),
        (
            iamraw.sections.Appendix,
            (76, 90),
            [],
        ),
    ]
}
