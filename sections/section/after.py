# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import inspect

import iamraw
import iamraw.sections
import utila


def determine_document_section(
    current: iamraw.sections.DocumentSection,
    after: iamraw.sections.AreaItem,
):
    """It is not always required to change the `current` DocumentSection.

    We require only few DocumentSection, therefore in some cases more
    than one possible parent is defined.
    """
    if isinstance(current, (
            iamraw.sections.Appendix,
            iamraw.sections.Introduction,
    )):
        if isinstance(after, iamraw.MultipleSection):
            return current
    nextclass = MATCHING[type(after)]
    if inspect.isfunction(nextclass):
        # dynamic next section determiner
        nextclass = nextclass(after)
        return nextclass
    if isinstance(current, (
            iamraw.sections.MainPart,
            iamraw.sections.Unknown,
    )):
        changer = (
            iamraw.sections.AbbreviationTable,
            iamraw.sections.Appendix,
            iamraw.sections.FigureTable,
            iamraw.sections.Glossary,
            iamraw.sections.SymbolTable,
            iamraw.sections.TableTable,
        )
        if isinstance(after, changer):
            # TODO: HACK?
            return iamraw.sections.Appendix
    new_section = nextclass == iamraw.sections.DocumentSection
    use_current = (isinstance(nextclass, list) and
                   not any(item == current for item in nextclass))
    if new_section or use_current:
        if not current:
            return iamraw.sections.Unknown
        return current
    return nextclass


def multiplesection_next(multiple):
    if utila.select_type(multiple.content, iamraw.sections.Bibliography):
        return iamraw.sections.Appendix
    if utila.select_type(multiple.content, iamraw.sections.Appendix):
        return iamraw.sections.Appendix
    return iamraw.MultipleSection


# do not change DocumentSection
# iamraw.sections.DocumentSection
#       iamraw.sections.Text
#       iamraw.sections.WhitePage:
# yapf:disable
MATCHING = {
    iamraw.sections.Abstract: [  # pylint:disable=E1101
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Acknowledgments: [
        iamraw.sections.Introduction,
        iamraw.sections.Appendix,
    ],
    iamraw.sections.Appendix: [
        iamraw.sections.Appendix,
    ],
    iamraw.MultipleSection: multiplesection_next,
    iamraw.sections.AbbreviationTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Bibliography: iamraw.sections.Appendix,
    iamraw.sections.Chapter: iamraw.MainPart,
    iamraw.sections.FigureTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Index: iamraw.sections.Table,
    iamraw.sections.LegalInformation: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.TableOfContent: [
        iamraw.sections.Introduction,
        iamraw.sections.Table,
    ],
    iamraw.sections.SymbolTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.TableTable: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.Glossary: [
        iamraw.sections.Appendix,
        iamraw.sections.Introduction,
    ],
    iamraw.sections.CiteContent: iamraw.sections.CitePart,
    iamraw.sections.CitePart: iamraw.sections.CitePart,
    iamraw.sections.Text: iamraw.sections.DocumentSection,
    iamraw.sections.TitlePage: iamraw.sections.Introduction,
    iamraw.sections.WhitePage: iamraw.sections.DocumentSection,
}
# yapf:enable
