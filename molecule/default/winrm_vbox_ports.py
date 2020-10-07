"""
WinRM VBox Ports

- Python script to find current forwarded WinRM ports by reading Vagrant logs.
- This script should be ran in the `molecule prepare` phase.
- Outputs a `.winrm` file that contains the port per Molecule platform.
- The molecule.yml should be configured to utilize the correct `.winrm`
  file, which will set the appropriate `ansible_port` variable.
"""

import yaml
import os
import re
from os.path import expanduser

cwd = os.getcwd()
cwd_split = cwd.split('/')
role_index = cwd_split.index("molecule") - 1
role_dir_name = cwd_split[role_index]
home = expanduser("~")

molecule_yml_path = "{cwd}/molecule.yml".format(cwd=cwd)
molecule_cache_path = "{home}/.cache/molecule/{role_dir_name}/default".format(home=home,role_dir_name=role_dir_name)

with open(molecule_yml_path, 'r') as stream:
    try:
        molecule = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
stream.close()

platforms = []
for item in molecule["platforms"]:
    platforms.append(item["name"])

for platform in platforms:
    vagrant_log_path = "{c}/vagrant-{r}.out".format(c=molecule_cache_path,r=platform)
    vagrant_log_text = open(vagrant_log_path, "r").read()
    winrm_port = (re.findall("WinRM address.*", vagrant_log_text)[-1]).split(':')[-1]

    if winrm_port:
        f = open("{molecule_dir_path}/{platform}.winrm".format(molecule_dir_path=cwd,platform=platform),"w")
        f.write(winrm_port)
    f.close()
