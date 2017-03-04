import sys
import config
import utils
import json
import time
import hclinav

def navigate(argv):
    nav = hclinav.navigator(config.url, config.cliname)
    if len(argv) == 1:
        hclinav.for_help()

    length = len(argv[1:])
    for i, x in enumerate(argv[1:]):
        nav = hclinav.traverse_argument(nav, x)

        if i == length - 1:
            hclinav.traverse_execution(nav)

def cli():
    if len(sys.argv) > 2:
        if sys.argv[1] == "cli":
            config.parse_configuration(sys.argv[2])
            navigate(sys.argv[2:])

        elif sys.argv[1] == "create":
            config.create_configuration(sys.argv[2])
            config.alias_cli(sys.argv[2])

        elif sys.argv[1] == "help":
            hclinav.display_man_page(config.huckle_manpage_path)
            sys.exit(0)

        else:
            utils.eprint("huckle: " + sys.argv[1] + ": command not found.")
            hclinav.for_help()
            sys.exit(2)

    elif len(sys.argv) == 2:
        if sys.argv[1] == "--version":
            show_dependencies() 

        elif sys.argv[1] == "help":
            hclinav.display_man_page(config.huckle_manpage_path)
            sys.exit(0)

        else:
            utils.eprint("huckle: " + sys.argv[1] + ": command not found.")
            hclinav.for_help()
            sys.exit(2)
    else:
        hclinav.for_help()
        sys.exit(2)

def show_dependencies():
    dependencies = ""
    for i, x in enumerate(config.dependencies):
        dependencies += " "
        dependencies += config.dependencies[i].rsplit('==', 1)[0] + "/"
        dependencies += config.dependencies[i].rsplit('==', 1)[1]
    print "huckle/" + config.__version__ + dependencies

