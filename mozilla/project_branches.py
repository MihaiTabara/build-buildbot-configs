# noinspection PyInterpreter
PROJECT_BRANCHES = {
    ### PLEASE ADD NEW BRANCHES ALPHABETICALLY (twigs at the bottom, also alphabetically)
    # 'build-system': {},  # Bug 1010674
    #'fx-team': {},  #bug 1296396
    'mozilla-inbound': {
        'merge_builds': False,
        'repo_path': 'integration/mozilla-inbound',
        'enable_perproduct_builds': True,
        'mozconfig_dir': 'mozilla-central',
        'pgo_strategy': 'periodic',
        'periodic_start_hours': range(0, 24, 3),
        'talos_suites': {
            'xperf': 1,
        },
        'branch_projects': ['spidermonkey_tier_1'],
    },
    #'services-central': {},  # Bug 1010674
    # 'alder': {},
    # Bug 1252292 - Schedule e10s tests on Ash for all desktop platforms
    'ash': {
        'enable_talos': False,
        'lock_platforms': True,
        'merge_builds': False,
        'periodic_start_hours': [9, 21],
        'pgo_strategy': 'periodic',
        'platforms': {
            'linux': {
                'slave_platforms': ['ubuntu32_vm'],
            },
            'linux64': {
                'slave_platforms': ['ubuntu64_vm'],
            },
            'linux64-asan': {
                'slave_platforms': ['ubuntu64-asan_vm'],
            },
            'linux64-debug': {
                'slave_platforms': ['ubuntu64_vm'],
            },
            'macosx64': {
                'slave_platforms': ['yosemite_r7'],
            },
            'macosx64-debug': {
                'slave_platforms': ['yosemite_r7'],
            },
            'win32': {},
            'win32-debug': {},
            'win64': {},
            'win64-debug': {},
        },
    },
    'autoland': {
        'merge_builds': False,
        'repo_path': 'integration/autoland',
        'enable_perproduct_builds': True,
        'mozconfig_dir': 'mozilla-central',
        'pgo_strategy': 'periodic',
        'periodic_start_hours': range(0, 24, 3),
        'talos_suites': {
            'xperf': 1,
        },
        'branch_projects': ['spidermonkey_tier_1'],
    },
    #'birch': {},  # Bug 1010674
# Bug 1308544 - Enable automation jobs on Cedar twig
    'cedar': {
        'enable_perproduct_builds': False,
        'lock_platforms': True,
        'mozharness_tag': 'default',
        'enable_talos': True,
        'talos_suites': {
            'other': 1,
            'svgr': 1,
            'tp5o': 1,
            'other-e10s': 1,
            'svgr-e10s': 1,
            'tp5o-e10s': 1,
        },
        'enable_opt_unittests': True,
        'platforms': {
            'linux64': {},
            'linux64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
            'win64': {},
            'win64-debug': {},
        },
    },
    # Disabled by bug 1363047
    # 'cypress': {},
    'date': {
        'enable_talos': False,
        'lock_platforms': True,
        'merge_builds': False,
        'platforms': {
            'linux': {},
            'linux64': {},
            'linux64-debug': {},
            'android-api-15': {},
        },
    },
    # Disabled by bug 1363047
    # 'elm': {},
    # Disabled by Bug 1135702
    # 'fig': {},
    # Disabled by Bug 1206269
    # 'gum': {},
    # Disabled by bug 1363047
    # 'holly': {},

    'jamun': {
        'gecko_version': 53,
        'watch_all_branches': True,
        'desktop_mozharness_builds_enabled': True,
        'use_mozharness_repo_cache': False,
        'branch_projects': [],
        ## TODO - enabled tests.
        # note - to enable tests you must also remove:
        # platforms[platform]["slave_platforms"] item override below
        'enable_opt_unittests': False,
        'enable_debug_unittests': False,
        'enable_talos': True,
        ##
        'lock_platforms': True,
        'platforms': {
            # use default 'dep-signing' for now while in development
            'linux': {
                'dep_signing_servers': 'release-signing',
                "slave_platforms": [],
                "enable_dep": False,
            },
            'linux64': {
                'dep_signing_servers': 'release-signing',
                "slave_platforms": [],
                "enable_dep": False,
            },
            'win32': {
                'dep_signing_servers': 'release-signing',
                "slave_platforms": [],
            },
            'win64': {
                'dep_signing_servers': 'release-signing',
                "slave_platforms": [],
            },
            'macosx64': {
                'dep_signing_servers': 'release-signing',
                "slave_platforms": [],
            },
            'win32-devedition': {
                'dep_signing_servers': 'nightly-signing',
            },
            'win64-devedition': {
                'dep_signing_servers': 'nightly-signing',
            },
            'macosx64-devedition': {
                'dep_signing_servers': 'nightly-signing',
            },
            'linux64-debug': {
                "slave_platforms": [],
            },
            'linux64-asan': {
                "slave_platforms": [],
            },
            'linux64-asan-debug': {
                "slave_platforms": [],
            },
            'macosx64-debug': {
                "slave_platforms": [],
            },
            'win32-debug': {
                "slave_platforms": [],
            },
            'win64-debug': {
                "slave_platforms": [],
            },
            'android-api-15': {},
            'android-x86': {},
        },
        'pgo_strategy': 'per-checkin',
        'enable_release_promotion': {
            "firefox": True,
            "devedition": True,
        },
        'build_tools_repo_path': 'users/raliiev_mozilla.com/tools',
        "release_platforms": ("linux", "linux64", "win32", "win64", "macosx64"),
        "l10n_release_platforms": ("linux", "linux64", "win32", "win64", "macosx64"),
        "single_locale_branch_config": {
            "firefox": "dev-mozilla-beta",
            "devedition": "dev-mozilla-beta_devedition",
        },
        'release_channel_mappings': {
            "firefox": [["^.*$", ["beta-dev"]]],
            "devedition": [["^.*$", ["aurora-dev"]]],
        },
        'uptake_monitoring_platforms': {
            "firefox": ("linux", "linux64", "win32", "win64", "macosx64"),
            "fennec": ("android-api-15", "android-x86"),
            "devedition": ("linux", "linux64", "win32", "win64", "macosx64"),
        },
        # temp balrog
        'balrog_api_root': 'http://ec2-54-196-167-74.compute-1.amazonaws.com:7070/api',
        'funsize_balrog_api_root': 'http://ec2-54-196-167-74.compute-1.amazonaws.com:7070/api',
        'tuxedoServerUrl': 'https://admin-bouncer.stage.mozaws.net/api',
        'bouncer_submitter_config': {
            "firefox": "releases/bouncer_firefox_beta.py",
            "devedition": "releases/bouncer_firefox_devedition.py",
        },
        'bouncer_enabled': True,
        'updates_builder_enabled': True,
        'update_verify_enabled': True,
        'postrelease_version_bump_enabled': {
            "firefox": True,
            "devedition": False,
            "fennec": True,
        },
        'postrelease_version_bump_config': {
            "firefox": 'releases/dev_postrelease_firefox_beta.py',
            "devedition": 'disabled',
        },
        'uptake_monitoring_enabled': True,
        'uptake_monitoring_config': {
            "firefox": 'releases/bouncer_firefox_beta.py',
            "devedition": 'releases/bouncer_firefox_devedition.py',
        },
        'postrelease_bouncer_aliases_enabled': True,
        'postrelease_bouncer_aliases_config': {
            "firefox": 'releases/bouncer_firefox_beta.py',
            "devedition": 'releases/bouncer_firefox_devedition.py',
        },
        'postrelease_mark_as_shipped_enabled': True,
        'postrelease_mark_as_shipped_config': {
            "firefox": 'releases/dev_postrelease_firefox_beta.py',
            "devedition": 'releases/dev_postrelease_firefox_beta.py',
        },
        'push_to_candidates_enabled': True,
        'updates_config': {
            "firefox": 'releases/dev_updates_firefox_beta.py',
            "devedition": 'releases/dev_updates_firefox_devedition.py',
        },
        'beetmover_credentials': '/builds/dev-beetmover-s3.credentials',
        'beetmover_buckets': {
            'firefox': 'net-mozaws-stage-delivery-firefox',
            'devedition': 'net-mozaws-stage-delivery-archive',
        },
        'stage_product': {
            'firefox': 'firefox',
            'fennec': 'mobile',
            'devedition': 'devedition',
        },
        'signing_class': {
            "firefox": "release-signing",
            "devedition": "nightly-signing",
        },
        'signing_cert': {
            "firefox": "release",
            "devedition": "nightly",
        },
        'accepted_mar_channel_id': {
            "firefox": "firefox-mozilla-beta",
            "devedition": "firefox-mozilla-aurora",
        },
        'root_home_dir': {
            "firefox": "desktop",
            "devedition": "desktop",
        },
        'enabled_products': ['firefox', 'mobile', 'devedition'],
        'push_to_releases_automatic': False,
        'merge_builds': False,
        'snap_enabled': {"firefox": True, "devedition": False},
        'update_verify_channel': {
            'firefox': 'beta-dev-cdntest',
            'devedition': 'aurora-dev-cdntest',
        },
        'tc_indexes': {
            "firefox": {
                "linux": {
                    "signed": "gecko.v2.jamun.signed-nightly.revision.{rev}.firefox-l10n.linux-opt.en-US",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.firefox-l10n.linux-opt.en-US",
                },
                "linux64": {
                    "signed": "gecko.v2.jamun.signed-nightly.revision.{rev}.firefox-l10n.linux64-opt.en-US",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.firefox-l10n.linux64-opt.en-US",
                },
                "macosx64": {
                    "signed": "gecko.v2.jamun.revision.{rev}.firefox.macosx64-opt",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.firefox.macosx64-opt",
                },
                "win32": {
                    "signed": "gecko.v2.jamun.revision.{rev}.firefox.win32-opt",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.firefox.win32-opt",
                },
                "win64": {
                    "signed": "gecko.v2.jamun.revision.{rev}.firefox.win64-opt",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.firefox.win64-opt",
                },
            },
            "devedition": {
                "linux": {
                    "signed": "gecko.v2.jamun.signed-nightly.revision.{rev}.devedition-l10n.linux-opt.en-US",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.devedition-l10n.linux-opt.en-US",
                },
                "linux64": {
                    "signed": "gecko.v2.jamun.signed-nightly.revision.{rev}.devedition-l10n.linux64-opt.en-US",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.devedition-l10n.linux64-opt.en-US",
                },
                "macosx64": {
                    "signed": "gecko.v2.jamun.revision.{rev}.devedition.macosx64-opt",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.devedition.macosx64-opt",
                },
                "win32": {
                    "signed": "gecko.v2.jamun.revision.{rev}.devedition.win32-opt",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.devedition.win32-opt",
                },
                "win64": {
                    "signed": "gecko.v2.jamun.revision.{rev}.devedition.win64-opt",
                    "unsigned": "gecko.v2.jamun.revision.{rev}.devedition.win64-opt",
                },
            },
            # TODO: fennec
        },
    },
    'larch': {
        'lock_platforms': True,
        'pgo_strategy': 'per-checkin',
        'platforms': {
            'linux': {},
            'linux64': {},
            'linux64-asan': {},
            'linux64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
            'win32': {},
            'win32-debug': {},
            'win64': {},
            'win64-debug': {},
        },
    },
    # disabled in bug 1215527
    # 'maple': {},
    # customizations for integration work for bugs 481815 and 307181
    'oak': {
        'enable_nightly': True,
        'updates_enabled': True,
        'create_partial': True,
        'enable_talos': False,
        'pgo_strategy': 'periodic',
        'platforms': {
            'linux': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'linux64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'macosx64': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win32': {
                'nightly_signing_servers': 'nightly-signing',
            },
            'win64': {
                'nightly_signing_servers': 'nightly-signing',
            },
        },
    },
    # Not needed whilst booked for bug 929203.
    'pine': {
        'enable_perproduct_builds': False,
        'lock_platforms': True,
        'mozharness_tag': 'default',
        'enable_opt_unittests': True,
        'enable_talos': True,
        'platforms': {
            'linux64': {},
            'linux64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
            'win64': {},
            'win64-debug': {},
        },
    },
    'graphics': {
        'enable_perproduct_builds': False,
        'lock_platforms': True,
        'mozharness_tag': 'default',
        'enable_opt_unittests': True,
        'enable_talos': False,
        'platforms': {
            'linux64': {},
            'linux64-debug': {},
            'macosx64': {},
            'macosx64-debug': {},
            'win64': {},
            'win64-debug': {},
        },
    },
}

# All is the default
ACTIVE_PROJECT_BRANCHES = PROJECT_BRANCHES.keys()

# Load up project branches' local values
for branch in PROJECT_BRANCHES.keys():
    PROJECT_BRANCHES[branch]['tinderbox_tree'] = PROJECT_BRANCHES[branch].get('tinderbox_tree', branch.title())
    PROJECT_BRANCHES[branch]['mobile_tinderbox_tree'] = PROJECT_BRANCHES[branch].get('mobile_tinderbox_tree', branch.title())
