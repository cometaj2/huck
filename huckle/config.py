from ConfigParser import SafeConfigParser
from StringIO import StringIO

# huckle's imports
from . import hutils

import os
import sys

__version__ = "0.4.1"
dependencies = ["restnavigator==1.0.1",
                "requests[socks]==2.13.0"]

root = os.path.abspath(os.path.dirname(__file__))
huckle_manpage_path = root + "/data/huckle.1"
home = os.path.expanduser("~")
dot_huckle = "%s/.huckle" % home
dot_huckle_profile = dot_huckle + "/huckle_profile"
dot_bash_profile = home + "/.bash_profile"

# These next 3 variables are dynamically updated from read configuration. Be careful!
url = ""
cliname = ""
cli_manpage_path = "/tmp"

# These hcli_ variables are taken from the semantic types found in the HCLI 1.0 specification
hcli_command_type = "command"
hcli_option_type = "option"
hcli_parameter_type = "parameter"
hcli_safe_type = "safe-execution"
hcli_unsafe_type = "unsafe-execution"

# parses the configuration of a given cli to set configured execution
def parse_configuration(cli):
    config_file_path = dot_huckle + "/" + cli + "/config"
    parser = SafeConfigParser()
    parser.read(config_file_path)
    if parser.has_section("default"):
        for section_name in parser.sections():
            for name, value in parser.items("default"):
                if name == "url":
                    global url
                    url = value
                    global cliname
                    cliname = cli
                    global cli_manpage_path
                    cli_manpage_path = cli_manpage_path + "/huckle." + cliname
            if url == "": sys.exit("No url defined for " + cli + " under " + config_file_path)
    else:
        sys.exit("No cli configuration " + config_file_path + " available for " + cli) 

# creates a configuration file for a named cli
def create_configuration(cli):
    config_file_folder = dot_huckle + "/" + cli 
    config_file = config_file_folder + "/config"
    hutils.create_folder(config_file_folder)
    
    if not os.path.exists(config_file):
        hutils.create_file(config_file)
        init_configuration(cli)

    hutils.create_folder(cli_manpage_path + "/huckle." + cli)

# sets up an alias for a cli so that it can be called directly by name (instead of calling it via the explicit huckle call) 
def alias_cli(cli):
    if not is_configured(dot_bash_profile, ". " + dot_huckle_profile):
        f = open(dot_bash_profile, "a+")
        f.write("\n")
        f.write("# we load the huckle aliases profile\n")
        f.write(". " + dot_huckle_profile)
        f.close

    if not is_configured(dot_huckle_profile, "alias " + cli + "="):
        g = open(dot_huckle_profile, "a+")
        g.write("alias " + cli + "=\"huckle cli " + cli + "\"\n")
        g.close

# initializes the configuration file of a given cli (initialized when a cli "created")
def init_configuration(cli):
    config_file_path = dot_huckle + "/" + cli + "/config"
    parser = SafeConfigParser()
    parser.readfp(StringIO("[default]"))
    parser.set("default", "url", "")
      
    with open(config_file_path, "w") as config:
        parser.write(config)

# verifies if a given configuration exists
def is_configured(file_path, contains):
    if contains in open(file_path).read():
        return True
    else:
        return False
