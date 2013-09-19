from copy import deepcopy

import config_common
reload(config_common)
from config_common import TALOS_CMD, loadDefaultValues, loadCustomTalosSuites, loadTalosSuites

import master_common
reload(master_common)
from master_common import setMainFirefoxVersions, items_before

import project_branches
reload(project_branches)
from project_branches import PROJECT_BRANCHES, ACTIVE_PROJECT_BRANCHES

import localconfig
reload(localconfig)
from localconfig import SLAVES, TRY_SLAVES, GLOBAL_VARS, GRAPH_CONFIG
from config import MOZHARNESS_REBOOT_CMD

TALOS_REMOTE_FENNEC_OPTS = {'productName': 'fennec',
                            'remoteTests': True,
                            'remoteExtras': {'options': ['--sampleConfig', 'remote.config',
                                                         '--output', 'local.yml',
                                                         '--webServer', 'bm-remote.build.mozilla.org',
                                                         '--browserWait', '60',
                                                         ],
                                             },
                            }

ANDROID_UNITTEST_REMOTE_EXTRAS = {'cmdOptions': ['--bootstrap'], }

BRANCHES = {
    'mozilla-central':     {},
    'mozilla-aurora':      {},
    'mozilla-release':     {},
    'mozilla-beta':        {},
    'mozilla-esr17':       {
        'datazilla_url': None,
        'gecko_version': 17,
        'platforms': {},
        'lock_platforms': True,
    },
    'mozilla-b2g18': {
        'datazilla_url': None,
        'gecko_version': 18,
        'platforms': {
            'android-noion': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g18_v1_0_1': {
        'datazilla_url': None,
        'gecko_version': 18,
        'platforms': {
            'android-noion': {},
        },
        'lock_platforms': True,
    },
    'mozilla-b2g18_v1_1_0_hd': {
        'datazilla_url': None,
        'gecko_version': 18,
        'platforms': {
            'android-noion': {},
        },
        'lock_platforms': True,
    },
    'try': {'coallesce_jobs': False},
}

setMainFirefoxVersions(BRANCHES)

# Talos
PLATFORMS = {
    'android': {},
    'android-armv6': {},
    'android-noion': {},
    'android-x86': {},
}

PLATFORMS['android']['slave_platforms'] = ['tegra_android', 'panda_android', 'panda_android-nomozpool']
PLATFORMS['android']['env_name'] = 'android-perf'
PLATFORMS['android']['is_mobile'] = True
PLATFORMS['android']['tegra_android'] = {'name': "Android 2.2 Tegra",
                                         'mozharness_talos': False,
                                         }
PLATFORMS['android']['panda_android'] = {'name': "Android 4.0 Panda",
                                         'mozharness_talos': True,
                                         }
PLATFORMS['android']['panda_android-nomozpool'] = {'name': "Android 4.0 Panda",
                                                   'mozharness_talos': True,
                                                   }
PLATFORMS['android']['stage_product'] = 'mobile'
PLATFORMS['android']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
    'talos_script_maxtime': 10800,
}

PLATFORMS['android-armv6']['slave_platforms'] = ['tegra_android-armv6']
PLATFORMS['android-armv6']['env_name'] = 'android-perf'
PLATFORMS['android-armv6']['is_mobile'] = True
PLATFORMS['android-armv6']['tegra_android-armv6'] = {'name': "Android 2.2 Armv6 Tegra"}
PLATFORMS['android-armv6']['stage_product'] = 'mobile'
PLATFORMS['android-armv6']['mozharness_config'] = {}

PLATFORMS['android-noion']['slave_platforms'] = ['tegra_android-noion']
PLATFORMS['android-noion']['env_name'] = 'android-perf'
PLATFORMS['android-noion']['is_mobile'] = True
PLATFORMS['android-noion']['tegra_android-noion'] = {'name': "Android 2.2 no-ionmonkey Tegra"}
PLATFORMS['android-noion']['stage_product'] = 'mobile'
PLATFORMS['android-noion']['mozharness_python'] = '/tools/buildbot/bin/python'

PLATFORMS['android-x86']['slave_platforms'] = ['ubuntu64_hw']
PLATFORMS['android-x86']['env_name'] = 'android-perf'
PLATFORMS['android-x86']['is_mobile'] = True
PLATFORMS['android-x86']['ubuntu64_hw'] = {'name': "Android 4.2 x86 Emulator"}
PLATFORMS['android-x86']['stage_product'] = 'mobile'
PLATFORMS['android-x86']['mozharness_config'] = {
    'mozharness_python': '/tools/buildbot/bin/python',
    'hg_bin': 'hg',
    'reboot_command': ['/tools/buildbot/bin/python'] + MOZHARNESS_REBOOT_CMD,
}

# Lets be explicit instead of magical.
for platform, platform_config in PLATFORMS.items():
    for slave_platform in platform_config['slave_platforms']:
        platform_config[slave_platform]['slaves'] = sorted(SLAVES[slave_platform])
        if slave_platform in TRY_SLAVES:
            platform_config[slave_platform]['try_slaves'] = sorted(TRY_SLAVES[slave_platform])
        else:
            platform_config[slave_platform]['try_slaves'] = platform_config[slave_platform]['slaves']

ANDROID = PLATFORMS['android']['slave_platforms']
ANDROID_NOT_MOZPOOL = deepcopy(ANDROID)
if 'panda_android-nomozpool' in PLATFORMS['android']['slave_platforms']:
    ANDROID_NOT_MOZPOOL.remove('panda_android')

SUITES = {
    'remote-ts': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'ts', '--mozAfterPaint', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-tsvg': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvg', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-tsvgx': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsvgx', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-tcanvasmark': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tcanvasmark', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-tsspider': {
        'enable_by_default': False,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tsspider', '--noChrome'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-trobopan': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'trobopan', '--noChrome', '--fennecIDs', '../fennec_ids.txt'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-troboprovider': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tprovider', '--noChrome', '--fennecIDs', '../fennec_ids.txt'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-trobocheck2': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tcheck2', '--noChrome', '--fennecIDs', '../fennec_ids.txt'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
    'remote-tp4m_nochrome': {
        'enable_by_default': True,
        'suites': GRAPH_CONFIG + ['--activeTests', 'tp4m', '--noChrome', '--rss'],
        'options': (TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL),
    },
}

BRANCH_UNITTEST_VARS = {
    'hghost': 'hg.mozilla.org',
    # turn on platforms as we get them running
    'platforms': {
        'android': {},
        'android-armv6': {},
        'android-noion': {},
        'android-debug': {},
        'android-x86': {},
    },
}

EMPTY_UNITTEST_DICT = {'opt_unittest_suites': [], 'debug_unittest_suites': []}

ANDROID_UNITTEST_DICT = {
    'opt_unittest_suites': [
        ('mochitest-1', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 1,
             },
        )),
        ('mochitest-2', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 2,
             },
        )),
        ('mochitest-3', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 3,
             },
        )),
        ('mochitest-4', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 4,
             },
        )),
        ('mochitest-5', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 5,
             },
        )),
        ('mochitest-6', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 6,
             },
        )),
        ('mochitest-7', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 7,
             },
        )),
        ('mochitest-8', (
            {'suite': 'mochitest-plain',
             'testManifest': 'android.json',
             'totalChunks': 8,
             'thisChunk': 8,
             },
        )),
        ('reftest-1', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 1,
             },
        )),
        ('reftest-2', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 2,
             },
        )),
        ('reftest-3', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 3,
             },
        )),
        ('reftest-4', (
            {'suite': 'reftest',
             'totalChunks': 4,
             'thisChunk': 4,
             },
        )),
        ('crashtest', (
            {'suite': 'crashtest',
             },
        )),
        ('xpcshell', (
            {'suite': 'xpcshell',
             },
        )),
        ('jsreftest-1', (
            {'suite': 'jsreftest',
             'totalChunks': 3,
             'thisChunk': 1,
             },
        )),
        ('jsreftest-2', (
            {'suite': 'jsreftest',
             'totalChunks': 3,
             'thisChunk': 2,
             },
        )),
        ('jsreftest-3', (
            {'suite': 'jsreftest',
             'totalChunks': 3,
             'thisChunk': 3,
             },
        )),
        ('robocop', (
            {'suite': 'mochitest-robocop',
             },
        )),
        ('mochitest-gl', (
            {'suite': 'mochitest-plain',
             'testPath': 'content/canvas/test/webgl',
             },
        )),
    ],
    'debug_unittest_suites': [],
}

ANDROID_MOZHARNESS_MOCHITEST = [
    ('mochitest-1',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-1'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-2',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-2'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-3',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-3'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-4',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-4'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-5',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-5'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-6',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-6'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-7',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-7'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('mochitest-8',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-8'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_REFTEST = [
    ('reftest-1',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-1'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('reftest-2',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-2'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('reftest-3',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-3'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('reftest-4',
     {'suite': 'reftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-4'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]
ANDROID_MOZHARNESS_CRASHTEST = [
    ('crashtest',
     {'suite': 'crashtest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--crashtest-suite', 'crashtest'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_JSREFTEST = [
    ('jsreftest-1',
     {'suite': 'jsreftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jsreftest-suite', 'jsreftest-1'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('jsreftest-2',
     {'suite': 'jsreftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jsreftest-suite', 'jsreftest-2'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('jsreftest-3',
     {'suite': 'jsreftest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jsreftest-suite', 'jsreftest-3'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_XPCSHELL = [
    ('xpcshell',
     {'suite': 'xpcshell',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--xpcshell-suite', 'xpcshell'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_MOCHITESTGL = [
    ('mochitest-gl',
     {'suite': 'mochitest-plain',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--mochitest-suite', 'mochitest-gl'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_PLAIN_REFTEST = [
    ('plain-reftest-1',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-1'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-2',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-2'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-3',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-3'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-4',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-4'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('plain-reftest-5',
     {'suite': 'reftestsmall',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--reftest-suite', 'reftest-5'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_JITTEST = [
    ('jittest',
     {'suite': 'jittest',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--jittest-suite', 'jittest'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_MOZHARNESS_PLAIN_ROBOCOP = [
    ('robocop-1',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-1'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('robocop-2',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-2'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
    ('robocop-3',
     {'suite': 'mochitest-robocop',
      'use_mozharness': True,
      'script_path': 'scripts/android_panda.py',
      'extra_args': ['--cfg', 'android/android_panda_releng.py', '--robocop-suite', 'robocop-3'],
      'timeout': 2400,
      'script_maxtime': 14400,
      },
     ),
]

ANDROID_NOION_UNITTEST_DICT = {
    'opt_unittest_suites': [],
    'debug_unittest_suites': [],
}
for suite in ANDROID_UNITTEST_DICT['opt_unittest_suites']:
    if not suite[0].startswith('jsreftest'):
        continue
    ANDROID_NOION_UNITTEST_DICT['opt_unittest_suites'].append(suite)

ANDROID_PLAIN_UNITTEST_DICT = {
    'opt_unittest_suites': [],
    'debug_unittest_suites': [],
}

TEGRA_RELEASE_PLAIN_UNITTEST_DICT = {
    'opt_unittest_suites': [],
    'debug_unittest_suites': [],
}

ANDROID_PLAIN_REFTEST_DICT = {
    'opt_unittest_suites': [
        ('plain-reftest-1', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 1,
             'extra_args': '--ignore-window-size'
             },
        )),
        ('plain-reftest-2', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 2,
             'extra_args': '--ignore-window-size'
             },
        )),
        ('plain-reftest-3', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 3,
             'extra_args': '--ignore-window-size'
             },
        )),
        ('plain-reftest-4', (
            {'suite': 'reftestsmall',
             'totalChunks': 4,
             'thisChunk': 4,
             'extra_args': '--ignore-window-size'
             },
        )),
    ],
}


ANDROID_PLAIN_ROBOCOP_DICT = {
    'opt_unittest_suites': [
        ('robocop-1', (
            {'suite': 'mochitest-robocop',
             'totalChunks': 2,
             'thisChunk': 1
             },
        )),
        ('robocop-2', (
            {'suite': 'mochitest-robocop',
             'totalChunks': 2,
             'thisChunk': 2
             },
        )),
    ],
}

for suite in ANDROID_UNITTEST_DICT['opt_unittest_suites']:
    if suite[0].startswith('reftest'):
        continue
    if suite[0].startswith('robocop'):
        continue
    ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

ANDROID_MOZHARNESS_PANDA_UNITTEST_DICT = {
    'opt_unittest_suites': ANDROID_MOZHARNESS_MOCHITEST + ANDROID_MOZHARNESS_PLAIN_ROBOCOP + ANDROID_MOZHARNESS_JSREFTEST + ANDROID_MOZHARNESS_CRASHTEST + ANDROID_MOZHARNESS_MOCHITESTGL + ANDROID_MOZHARNESS_PLAIN_REFTEST + ANDROID_MOZHARNESS_XPCSHELL + ANDROID_MOZHARNESS_JITTEST,
    'debug_unittest_suites': ANDROID_MOZHARNESS_MOCHITEST + ANDROID_MOZHARNESS_PLAIN_ROBOCOP + ANDROID_MOZHARNESS_JSREFTEST + ANDROID_MOZHARNESS_CRASHTEST + ANDROID_MOZHARNESS_MOCHITESTGL + ANDROID_MOZHARNESS_JITTEST,
}

for suite in ANDROID_UNITTEST_DICT['opt_unittest_suites']:
    if suite[0].startswith('reftest'):
        continue
    if suite[0].startswith('mochitest-gl'):
        continue
    if suite[0].startswith('robocop'):
        continue
    TEGRA_RELEASE_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

for suite in ANDROID_PLAIN_REFTEST_DICT['opt_unittest_suites']:
    ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)
    TEGRA_RELEASE_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

for suite in ANDROID_PLAIN_ROBOCOP_DICT['opt_unittest_suites']:
    ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)
    TEGRA_RELEASE_PLAIN_UNITTEST_DICT['opt_unittest_suites'].append(suite)

ANDROID_NOWEBGL_UNITTEST_DICT = deepcopy(ANDROID_PLAIN_UNITTEST_DICT)
# Bug 869590 Disable mochitest-gl for armv6, Bug 875633 Disable for Tegras
for suite in ANDROID_NOWEBGL_UNITTEST_DICT['opt_unittest_suites'][:]:
    if suite[0] == 'mochitest-gl':
        ANDROID_NOWEBGL_UNITTEST_DICT['opt_unittest_suites'].remove(suite)

ANDROID_PLAIN_UNITTEST_DICT['debug_unittest_suites'] = deepcopy(ANDROID_PLAIN_UNITTEST_DICT['opt_unittest_suites'])

# Beginning Androidx86 configurations
ANDROID_X86_MOZHARNESS_DICT = [
    ('androidx86-set-1', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'mochitest-1',
            '--test-suite', 'mochitest-2',
            '--test-suite', 'mochitest-4',
            '--test-suite', 'xpcshell',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
    ('androidx86-set-2', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'mochitest-5',
            '--test-suite', 'mochitest-6',
            '--test-suite', 'mochitest-7',
            '--test-suite', 'mochitest-8',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
]

ANDROID_X86_NOT_GREEN_DICT = [
    ('androidx86-set-3', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'reftest-1',
            '--test-suite', 'reftest-2',
            '--test-suite', 'reftest-3',
            '--test-suite', 'reftest-4',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
    ('androidx86-set-4', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'reftest-5',
            '--test-suite', 'reftest-6',
            '--test-suite', 'reftest-7',
            '--test-suite', 'reftest-8',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
    ('androidx86-set-5', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'reftest-9',
            '--test-suite', 'reftest-10',
            '--test-suite', 'jsreftest-1',
            '--test-suite', 'jsreftest-2',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
    ('androidx86-set-6', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'jsreftest-3',
            '--test-suite', 'jsreftest-4',
            '--test-suite', 'jsreftest-5',
            '--test-suite', 'jsreftest-6',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
    ('androidx86-set-7', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'crashtest-1',
            '--test-suite', 'crashtest-2',
            '--test-suite', 'crashtest-3',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
    ('androidx86-set-8', {
        'use_mozharness': True,
        'script_path': 'scripts/androidx86_emulator_unittest.py',
        'extra_args': [
            '--cfg', 'android/androidx86.py',
            '--test-suite', 'mochitest-3',
            '--test-suite', 'mochitest-gl',
            '--test-suite', 'robocop-1',
            '--test-suite', 'robocop-2',
        ],
        'timeout': 2400,
        'script_maxtime': 14400,
        },
    ),
]

# Funky DICT naming
ANDROID_X86_MOZHARNESS_UNITTEST_DICT = {
   'opt_unittest_suites': ANDROID_X86_MOZHARNESS_DICT,
   'debug_unittest_suites': [],
}
# End of Androidx86 configurations

# You must define opt_unittest_suites when enable_opt_unittests is True for a
# platform. Likewise debug_unittest_suites for enable_debug_unittests
PLATFORM_UNITTEST_VARS = {
    'android': {
        'product_name': 'fennec',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'is_remote': True,
        'host_utils_url': 'http://bm-remote.build.mozilla.org/tegra/tegra-host-utils.%%(foopy_type)s.742597.zip',
        'enable_opt_unittests': True,
        'enable_debug_unittests': True,
        'remote_extras': ANDROID_UNITTEST_REMOTE_EXTRAS,
        'tegra_android': deepcopy(ANDROID_NOWEBGL_UNITTEST_DICT),
        'panda_android': deepcopy(ANDROID_MOZHARNESS_PANDA_UNITTEST_DICT),
        'panda_android-nomozpool': deepcopy(EMPTY_UNITTEST_DICT),
    },
    'android-armv6': {
        'product_name': 'fennec',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'is_remote': True,
        'host_utils_url': 'http://bm-remote.build.mozilla.org/tegra/tegra-host-utils.%%(foopy_type)s.742597.zip',
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'remote_extras': ANDROID_UNITTEST_REMOTE_EXTRAS,
        'tegra_android-armv6': deepcopy(ANDROID_NOWEBGL_UNITTEST_DICT),
    },
    'android-noion': {
        'product_name': 'fennec',
        'app_name': 'browser',
        'brand_name': 'Minefield',
        'is_remote': True,
        'host_utils_url': 'http://bm-remote.build.mozilla.org/tegra/tegra-host-utils.%%(foopy_type)s.742597.zip',
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'remote_extras': ANDROID_UNITTEST_REMOTE_EXTRAS,
        'tegra_android-noion': deepcopy(ANDROID_NOION_UNITTEST_DICT),
    },
    'android-x86': {
        'product_name': 'fennec',
        'enable_opt_unittests': True,
        'enable_debug_unittests': False,
        'ubuntu64_hw': deepcopy(ANDROID_X86_MOZHARNESS_UNITTEST_DICT),
    },
}

# Copy project branches into BRANCHES keys
for branch in ACTIVE_PROJECT_BRANCHES:
    BRANCHES[branch] = deepcopy(PROJECT_BRANCHES[branch])
    if BRANCHES[branch].get('mobile_platforms'):
        BRANCHES[branch]['platforms'] = deepcopy(BRANCHES[branch]['mobile_platforms'])

# Copy unittest vars in first, then platform vars
for branch in BRANCHES.keys():
    for key, value in GLOBAL_VARS.items():
        # In order to have things ride the trains we need to be able to
        # override "global" things. Therefore, we shouldn't override anything
        # that's already been set.
        if key in BRANCHES[branch]:
            continue
        BRANCHES[branch][key] = deepcopy(value)

    for key, value in BRANCH_UNITTEST_VARS.items():
        # Don't override platforms if it's set and locked
        if key == 'platforms' and 'platforms' in BRANCHES[branch] and BRANCHES[branch].get('lock_platforms'):
            continue
        BRANCHES[branch][key] = deepcopy(value)

    for platform, platform_config in PLATFORM_UNITTEST_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

    # Copy in local config
    if branch in localconfig.BRANCHES:
        for key, value in localconfig.BRANCHES[branch].items():
            if key == 'platforms':
                # Merge in these values
                if 'platforms' not in BRANCHES[branch]:
                    BRANCHES[branch]['platforms'] = {}

                for platform, platform_config in value.items():
                    for key, value in platform_config.items():
                        value = deepcopy(value)
                        if isinstance(value, str):
                            value = value % locals()
                        BRANCHES[branch]['platforms'][platform][key] = value
            else:
                BRANCHES[branch][key] = deepcopy(value)

    # Merge in any project branch config for platforms
    if branch in ACTIVE_PROJECT_BRANCHES and 'mobile_platforms' in PROJECT_BRANCHES[branch]:
        for platform, platform_config in PROJECT_BRANCHES[branch]['mobile_platforms'].items():
            if platform in PLATFORMS:
                for key, value in platform_config.items():
                    value = deepcopy(value)
                    if isinstance(value, str):
                        value = value % locals()
                    BRANCHES[branch]['platforms'][platform][key] = value

    for platform, platform_config in localconfig.PLATFORM_VARS.items():
        if platform in BRANCHES[branch]['platforms']:
            for key, value in platform_config.items():
                value = deepcopy(value)
                if isinstance(value, str):
                    value = value % locals()
                BRANCHES[branch]['platforms'][platform][key] = value

#
# Entries in BRANCHES for tests should be a tuple of:
# - Number of tests to run per build
# - Whether queue merging is on
# - TalosFactory options
# - Which platforms to run on

# Let's load the defaults
for branch in BRANCHES.keys():
    BRANCHES[branch]['repo_path'] = branch
    BRANCHES[branch]['branch_name'] = branch.title()
    BRANCHES[branch]['mobile_branch_name'] = branch.title()
    BRANCHES[branch]['build_branch'] = branch.title()
    BRANCHES[branch]['enable_unittests'] = True
    BRANCHES[branch]['talos_command'] = TALOS_CMD
    BRANCHES[branch]['fetch_symbols'] = True
    BRANCHES[branch]['fetch_release_symbols'] = False
    BRANCHES[branch]['talos_from_source_code'] = True
    BRANCHES[branch]['support_url_base'] = 'http://talos-bundles.pvt.build.mozilla.org'
    loadTalosSuites(BRANCHES, SUITES, branch)
    BRANCHES[branch]['pgo_strategy'] = None
    BRANCHES[branch]['pgo_platforms'] = []

# The following are exceptions to the defaults

######## mozilla-central
BRANCHES['mozilla-central']['branch_name'] = "Firefox"
BRANCHES['mozilla-central']['repo_path'] = "mozilla-central"
BRANCHES['mozilla-central']['mobile_branch_name'] = "Mobile"
BRANCHES['mozilla-central']['mobile_talos_branch'] = "mobile"
BRANCHES['mozilla-central']['build_branch'] = "1.9.2"
BRANCHES['mozilla-central']['pgo_strategy'] = 'periodic'
BRANCHES['mozilla-central']['pgo_platforms'] = []
BRANCHES['mozilla-central']['platforms']['android']['enable_debug_unittests'] = True
BRANCHES['mozilla-central']['remote-tsvgx_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL)
BRANCHES['mozilla-central']['remote-tcanvasmark_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID_NOT_MOZPOOL)

######### mozilla-release
BRANCHES['mozilla-release']['release_tests'] = 1
BRANCHES['mozilla-release']['repo_path'] = "releases/mozilla-release"
BRANCHES['mozilla-release']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-release']['pgo_platforms'] = []
# MERGE DAY: Remove this line when FF26 merges in
BRANCHES['mozilla-release']['platforms']['android-x86']['enable_opt_unittests'] = False
# MERGE DAY: end

######### mozilla-beta
BRANCHES['mozilla-beta']['release_tests'] = 1
BRANCHES['mozilla-beta']['repo_path'] = "releases/mozilla-beta"
BRANCHES['mozilla-beta']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-beta']['pgo_platforms'] = []
# MERGE DAY: Remove this line when FF26 merges in
BRANCHES['mozilla-beta']['platforms']['android-x86']['enable_opt_unittests'] = False
# MERGE DAY: end

######### mozilla-aurora
BRANCHES['mozilla-aurora']['repo_path'] = "releases/mozilla-aurora"
BRANCHES['mozilla-aurora']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-aurora']['pgo_platforms'] = []
# MERGE DAY: Remove this line when FF26 merges in
BRANCHES['mozilla-aurora']['platforms']['android-x86']['enable_opt_unittests'] = False
# MERGE DAY: end

######### mozilla-esr17
BRANCHES['mozilla-esr17']['release_tests'] = 5
BRANCHES['mozilla-esr17']['repo_path'] = "releases/mozilla-esr17"
BRANCHES['mozilla-esr17']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-esr17']['pgo_platforms'] = []

######### mozilla-b2g18
BRANCHES['mozilla-b2g18']['release_tests'] = 1
BRANCHES['mozilla-b2g18']['repo_path'] = "releases/mozilla-b2g18"
BRANCHES['mozilla-b2g18']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g18']['pgo_platforms'] = []

######### mozilla-b2g18_v1_0_1
BRANCHES['mozilla-b2g18_v1_0_1']['release_tests'] = 1
BRANCHES['mozilla-b2g18_v1_0_1']['repo_path'] = "releases/mozilla-b2g18_v1_0_1"
BRANCHES['mozilla-b2g18_v1_0_1']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g18_v1_0_1']['pgo_platforms'] = []

######### mozilla-b2g18_v1_1_0_hd
BRANCHES['mozilla-b2g18_v1_1_0_hd']['release_tests'] = 1
BRANCHES['mozilla-b2g18_v1_1_0_hd']['repo_path'] = "releases/mozilla-b2g18_v1_1_0_hd"
BRANCHES['mozilla-b2g18_v1_1_0_hd']['pgo_strategy'] = 'per-checkin'
BRANCHES['mozilla-b2g18_v1_1_0_hd']['pgo_platforms'] = []

######## try
BRANCHES['try']['platforms']['android']['enable_debug_unittests'] = True
BRANCHES['try']['pgo_strategy'] = 'try'
BRANCHES['try']['pgo_platforms'] = []
BRANCHES['try']['enable_try'] = True

# Ignore robocop chunks for mozilla-release, robocop-chunks is defined in ANDROID_PLAIN_UNITTEST_DICT
BRANCHES['mozilla-release']["platforms"]["android"]["tegra_android"]["opt_unittest_suites"] = deepcopy(TEGRA_RELEASE_PLAIN_UNITTEST_DICT["opt_unittest_suites"])

######## generic branch variables for project branches
for projectBranch in ACTIVE_PROJECT_BRANCHES:
    branchConfig = PROJECT_BRANCHES[projectBranch]
    loadDefaultValues(BRANCHES, projectBranch, branchConfig)
    loadCustomTalosSuites(BRANCHES, SUITES, projectBranch, branchConfig)

# start temp fix until panda android pools are collapsed again in bug 913206    
BRANCHES['cedar']['remote-ts_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID)
BRANCHES['cedar']['remote-trobopan_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID)
BRANCHES['cedar']['remote-tp4m_nochrome_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID)
BRANCHES['cedar']['remote-troboprovider_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID)
BRANCHES['cedar']['remote-tsvg_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID)
BRANCHES['cedar']['remote-trobocheck2_tests'] = (1, True, TALOS_REMOTE_FENNEC_OPTS, ANDROID)

BRANCHES['cedar']['platforms']['android']['slave_platforms'] = ['tegra_android', 'panda_android']
# end temp fix until panda android pools are collapsed again in bug 913206

# Until we green out these Android x86 tests
BRANCHES['cedar']['platforms']['android-x86']['ubuntu64_hw']['opt_unittest_suites'] += ANDROID_X86_NOT_GREEN_DICT[:]
BRANCHES['ash']['platforms']['android-x86']['ubuntu64_hw']['opt_unittest_suites'] += ANDROID_X86_NOT_GREEN_DICT[:]

# XXX Bug 789373 hack - add android-noion until we have b2g testing
# Delete all references to android-noion once we have b2g jsreftests not
# in an emulator.
for branch in BRANCHES:
    if branch not in ('mozilla-central', 'mozilla-inbound', 'mozilla-b2g18',
                      'mozilla-b2g18_v1_0_1', 'mozilla-b2g18_v1_1_0_hd', 'try',
                      'b2g-inbound', 'date',
                      ):
        if 'android-noion' in BRANCHES[branch]['platforms']:
            del BRANCHES[branch]['platforms']['android-noion']

for name, branch in items_before(BRANCHES, 'gecko_version', 22):
    if 'android' in branch['platforms']:
        del branch['platforms']['android']['panda_android']
        del BRANCHES[branch]['platforms']['android']['panda_android-nomozpool']
        branch['platforms']['android']['slave_platforms'] = ['tegra_android']

# Do android debug only on cedar
for branch in BRANCHES:
    if branch not in ('cedar') and \
            'android' in BRANCHES[branch]['platforms'] and \
            'enable_debug_unittests' in BRANCHES[branch]['platforms']['android']:
        BRANCHES[branch]['platforms']['android']['enable_debug_unittests'] = False

# XPCShell (Gecko 23 based)
for name, branch in items_before(BRANCHES, 'gecko_version', 23):
    for platform in branch['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in branch['platforms'][platform]:
                continue
            for type in branch['platforms'][platform][slave_plat]:
                for suite in branch['platforms'][platform][slave_plat][type][:]:
                    if "xpcshell" in suite[0]:
                        branch['platforms'][platform][slave_plat][type].remove(suite)

# Panda XPCShell on try only
for branch in BRANCHES:
    # Loop removes it from any branch that gets beyond here
    if branch in ('try', 'mozilla-central', 'mozilla-inbound', 'fx-team', 'b2g-inbound'):
        continue

    for platform in BRANCHES[branch]['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in BRANCHES[branch]['platforms'][platform]:
                continue
            if not 'panda' in slave_plat:
                continue
            for type in BRANCHES[branch]['platforms'][platform][slave_plat]:
                for suite in BRANCHES[branch]['platforms'][platform][slave_plat][type][:]:
                    if "xpcshell" in suite[0]:
                        BRANCHES[branch]['platforms'][platform][slave_plat][type].remove(suite)

# Support reftests for pandaboards on Cedar and Try
for branch in BRANCHES:
    # Loop removes it from any branch that gets beyond here
    if branch in ('cedar', 'try'):
        continue
    for platform in BRANCHES[branch]['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in BRANCHES[branch]['platforms'][platform]:
                continue
            if not slave_plat == "panda_android":
                continue
            for type in BRANCHES[branch]['platforms'][platform][slave_plat]:
                for suite in BRANCHES[branch]['platforms'][platform][slave_plat][type][:]:
                    if ("plain-reftest" in suite[0]):
                        BRANCHES[branch]['platforms'][platform][slave_plat][type].remove(suite)

#only run mozharness talos with mozpool for Panda android tests on cedar 
for branch in BRANCHES:
    # Loop removes it from any branch that gets beyond here
    if branch in ('cedar', ):
        continue
    BRANCHES[branch]['mozharness_talos'] = False


# schedule jittests for pandas on cedar
# https://bugzilla.mozilla.org/show_bug.cgi?id=912997
for branch in BRANCHES:
    # Loop removes it from any branch that gets beyond here
    if branch in ('cedar', ):
        continue
    for platform in BRANCHES[branch]['platforms']:
        if not platform in PLATFORMS:
            continue
        if not platform.startswith('android'):
            continue
        if platform.endswith('-debug'):
            continue  # no slave_platform for debug
        for slave_plat in PLATFORMS[platform]['slave_platforms']:
            if not slave_plat in BRANCHES[branch]['platforms'][platform]:
                continue
            if not slave_plat == "panda_android":
                continue
            for type in BRANCHES[branch]['platforms'][platform][slave_plat]:
                for suite in BRANCHES[branch]['platforms'][platform][slave_plat][type][:]:
                    if ("jittest" in suite[0]):
                        BRANCHES[branch]['platforms'][platform][slave_plat][type].remove(suite)

if __name__ == "__main__":
    import sys
    import pprint

    args = sys.argv[1:]

    if len(args) > 0:
        items = dict([(b, BRANCHES[b]) for b in args])
    else:
        items = dict(BRANCHES.items())

    for k, v in sorted(items.iteritems()):
        out = pprint.pformat(v)
        for l in out.splitlines():
            print '%s: %s' % (k, l)

    for suite in sorted(SUITES):
        out = pprint.pformat(SUITES[suite])
        for l in out.splitlines():
            print '%s: %s' % (suite, l)
