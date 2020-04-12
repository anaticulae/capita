# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Workplan Runner
===============

Workplan
--------

.. code-block:: none

    [titlepage]
        char_margin = 10
        word_margin = 20

    [bibliography]
        char_margin = 100

    > titlepage

        > rawmaker -i abc.pdf -o extracted/titlepage --config titlepage.cfg
        > detector -i expected/titlepage -o detector_result --title --page=2

    > bibliography

        > rawmaker -i abc.pdf -o extracted/bibliography -c {bibliography}
        > detector -i expected/titlepage -o detector_result --bibliography --page=14:15

    > text ...
"""

import concurrent.futures
import os

import utila

import sections.workplan.serialize


def runtime(rawplan: str, cwd: str = None, worker: int = 12) -> int:
    splitted = sections.workplan.serialize.load_plan(rawplan)
    failure = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = {
            executor.submit(runlevel, name, cmd, cwd): name
            for name, cmd in splitted.cmds  # pylint:disable=E1133
        }
        for future in concurrent.futures.as_completed(futures):
            failure += future.result()
    return failure


def runlevel(name: str, cmd: str, cwd: str = None):
    utila.log(f'run: {name}')
    cmd = ' && '.join(cmd)
    utila.log(cmd)

    completed = utila.run(cmd, cwd, expect=None)

    msg = f'\n...........{name}...........\n'.center(60)
    msg += completed.stdout
    if completed.returncode:
        msg += '[ERROR]\n'
        msg += completed.stderr
    msg += f'\n-----------{name}-----------\n'.center(60)
    utila.log(msg)
    return completed.returncode


def setup_plan(plan: str, config: dict, validate: bool = True) -> str:
    """Fill template strings with absolute paths and configuration.

    >>> setup_plan(['>decider -i {RAWMAKER_INPUT} -o {OUTPUT}'],
    ... {'rawmaker_input' : 'source.txt', 'output' : 'output.txt'})
    '>decider -i source.txt -o output.txt'

    Hint: `>` is required to split config items from cmd items

    Returns:
        Fully replaced workplan template.
    Raises:
        ValueError: if not every template string is replaced
    """
    result = plan if isinstance(plan, str) else utila.NEWLINE.join(plan)
    result = replace_config_ini(result)

    # replace templates
    for key, value in config.items():
        if isinstance(value, dict):
            continue
        key = '{%s}' % key.upper()
        result = result.replace(key, value)

    if validate:
        if '{' in result or '}' in result:
            raise ValueError(f'template is not fully replaced:\n{result}')
    return result


def replace_config_ini(result):
    header, tailer = sections.workplan.serialize.divide_plan(result)
    variables = utila.load_config(header)
    if not variables:
        return tailer
    # replace configuration
    for header, sec in variables.items():
        pattern = '-c {%s}' % header.upper()
        param = ' '.join(['--%s=%s' % (key, val) for key, val in sec.items()])
        tailer = tailer.replace(pattern, param)
    return tailer


def setup_testfolder(
        path: str,
        source: str,
        config: str,
        dry: bool = True,
        verbose: bool = False,
) -> dict:
    if not dry:
        assert os.path.exists(source), str(source)
        assert os.path.exists(config), str(config)
        os.makedirs(path, exist_ok=True)

    result = {
        'source': source,
    }
    # configuration
    configuration = [
        'rawmaker_cfg_title',
        'rawmaker_cfg_title_oneline',
        'rawmaker_cfg_toc',
        'rawmaker_cfg_words',
        'rawmaker_cfg_bibliography',
        'rawmaker_cfg_bibliography_oneline',
    ]
    for item in configuration:
        cfg = os.path.join(config, f'{item}.ini')
        if not dry:
            assert os.path.exists(cfg), str(cfg)
        result[item] = cfg

    # folder
    items = [
        'rawmaker_title',
        'rawmaker_toc',
        'rawmaker_words',
        'rawmaker_bibliography',
        'detector_result',
        'groupme_result',
        'words_result',
    ]
    for item in items:
        current = os.path.join(path, item)
        if verbose:
            utila.log(f'create: {current}')
        if not dry:
            os.makedirs(current, exist_ok=True)
        result[item] = current

    # forward slash
    result = {
        key: utila.forward_slash(item, save_newline=False)
        for key, item in result.items()
    }
    return result
