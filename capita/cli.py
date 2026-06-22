#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import capita
import utilo

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

WORKPLAN = [
    utilo.create_step(
        'abbreviation',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'abstract',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.File(name='pdflog', optional=True),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'acknowledge',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'appendix',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'figuretable',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'glossary',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.File(name='pdflog', optional=True),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'index',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'legal',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'symboltable',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'tabletable',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'title',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'toc',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'whitepage',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.Directory('rawmaker__images_images'),
            utilo.Directory('rawmaker__figures_figures'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'chapter',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('rawmaker', 'outlines_outlines'),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'paper',
        inputs=[
            utilo.Value('pdf', typ=None, defaultvar=None),
        ],
        output=('likelihood',),
    ),
    utilo.create_step(
        'section',
        inputs=[
            utilo.ResultFile('sections', 'abbreviation_likelihood'),
            utilo.ResultFile('sections', 'abstract_likelihood'),
            utilo.ResultFile('sections', 'acknowledge_likelihood'),
            utilo.ResultFile('sections', 'appendix_likelihood'),
            utilo.ResultFile('sections_ref', 'bibliography_like'),
            utilo.ResultFile('sections', 'chapter_likelihood'),
            utilo.ResultFile('sections', 'figuretable_likelihood'),
            utilo.ResultFile('sections', 'index_likelihood'),
            utilo.ResultFile('sections', 'legal_likelihood'),
            utilo.ResultFile('sections', 'paper_likelihood'),
            utilo.ResultFile('sections', 'symboltable_likelihood'),
            utilo.ResultFile('sections', 'tabletable_likelihood'),
            utilo.ResultFile('sections', 'title_likelihood'),
            utilo.ResultFile('sections', 'toc_likelihood'),
            utilo.ResultFile('sections', 'whitepage_likelihood'),
            utilo.ResultFile('sections', 'glossary_likelihood'),
        ],
        output=('result',),
    ),
    utilo.create_step(
        'docinfo',
        inputs=[
            utilo.ResultFile('sections', 'section_result'),
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.File(name='pdflog', optional=True),
        ],
        output=('docinfo',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=capita.ROOT,
        featurepackage='capita.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=capita.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            profileflag=True,
            version=capita.__version__,
        ),
    )
