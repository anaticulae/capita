# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import sections

RESOURCES = os.path.join(sections.ROOT, 'tests/resources')

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
HOMEWORK = os.path.join(RESOURCES, 'homework')
MASTER = os.path.join(RESOURCES, 'master')
ORDER = os.path.join(RESOURCES, 'order')
TECHNICAL = os.path.join(RESOURCES, 'technical')

GENERATED = os.path.join(RESOURCES, 'generated')
# NO_TITLE = os.path.join(GENERATED, 'notitle')

RESTRUCT = os.path.join(GENERATED, 'restruct')
RESTRUCT_PDF = os.path.join(DOCU, 'restructuredtext.pdf')

HOWTO_PYPORTING = os.path.join(GENERATED, 'howto_pyporting')
HOWTO_PYPORTING_PDF = os.path.join(DOCU, 'howto_pyporting.pdf')
# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
HOWTO_PYPORTING_CHAPTER_PAGE_COUNT = 2

# porting module
PYPORTING = os.path.join(GENERATED, 'porting_module')
PYPORTING_PDF = os.path.join(DOCU, 'porting_extension_modules.pdf')

BACHELOR37 = os.path.join(GENERATED, 'page_37_tables')
BACHELOR37_PDF = os.path.join(BACHELOR, 'page_37_tables.pdf')

BACHELOR56 = os.path.join(GENERATED, 'page_56_hard_to_read')
BACHELOR56_PDF = os.path.join(BACHELOR, 'page_56_hard_to_read.pdf')

BACHELOR63 = os.path.join(GENERATED, 'page_63_images_toc')
BACHELOR63_PDF = os.path.join(BACHELOR, 'page_63_images_toc.pdf')

BACHELOR111 = os.path.join(GENERATED, 'page_111_images_toc')
BACHELOR111_PDF = os.path.join(BACHELOR, 'page_111_images_toc.pdf')

MASTER72 = os.path.join(GENERATED, 'page_72_noimages_toc')
MASTER72_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

MASTER98 = os.path.join(GENERATED, 'page98')
MASTER98_PDF = os.path.join(MASTER, 'page98.pdf')

MASTER116 = os.path.join(GENERATED, 'page_116_images_toc_formular')
MASTER116_PDF = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

HOWTO_ARGPARSE = os.path.join(GENERATED, 'howto_argparse')
HOWTO_ARGPARSE_PDF = os.path.join(DOCU, 'howto_argparse.pdf')

REQURIED_RESOURCES = [
    BACHELOR111,
    BACHELOR111_PDF,
    BACHELOR37,
    BACHELOR37_PDF,
    BACHELOR56,
    BACHELOR56_PDF,
    BACHELOR63,
    BACHELOR63_PDF,
    HOWTO_ARGPARSE,
    HOWTO_ARGPARSE_PDF,
    HOWTO_PYPORTING,
    HOWTO_PYPORTING_PDF,
    MASTER116,
    MASTER116_PDF,
    MASTER72,
    MASTER72_PDF,
    MASTER98,
    MASTER98_PDF,
    PYPORTING,
    PYPORTING_PDF,
    RESOURCES,
    RESTRUCT,
    RESTRUCT_PDF,
]

REQURIED_RESOURCES = [utila.forward_slash(item) for item in REQURIED_RESOURCES]
