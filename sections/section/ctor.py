# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.sections

# THE ORDER IS IMPORTANT!
BUILDER = [
    iamraw.sections.AbbreviationTable,
    iamraw.sections.Abstract,
    iamraw.sections.Acknowledgments,
    iamraw.sections.Appendix,
    iamraw.sections.Bibliography,
    iamraw.sections.Chapter,
    iamraw.sections.FigureTable,
    iamraw.sections.Index,
    iamraw.sections.LegalInformation,
    iamraw.sections.CiteContent,
    iamraw.sections.SymbolTable,
    iamraw.sections.TableTable,
    iamraw.sections.TitlePage,
    iamraw.sections.TableOfContent,
    iamraw.sections.WhitePage,
    iamraw.sections.Glossary,
]
assert BUILDER.index(iamraw.sections.TableOfContent) > BUILDER.index(
    iamraw.sections.TitlePage), 'do not sort BUILDER'


def create(start, end, trust, typ):
    ctor = BUILDER[typ]
    new = ctor(start=start, end=end, trust=trust)
    return new
