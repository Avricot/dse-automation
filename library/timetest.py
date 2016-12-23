#!/usr/bin/python

import datetime
import sys
import json
import os
import shlex
import subprocess
from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(argument_spec={
        "commands": {"required": True, "type": "list"}
    })

    commands = [{
            "command": "ulimit",
            "equals": 31}]
    module.params["commands"] = commands

    for command in commands:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        if("equals" in command):
            if len(lines) > 1:
                module.exit_json(changed=False, meta={"multi line"})
            if lines[0] == command["equals"]:
                module.exit_json(changed=False, meta={"OK": lines[0]})
            else:
                module.exit_json(changed=False, meta={"KO": lines[0]})
    #
    # response = {"hello": module.params}
    # module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()

# read the argument string from the arguments file
# args_file = sys.argv[1]
# args_data = file(args_file).read()
#
# # For this module, we're going to do key=value style arguments.
# # Modules can choose to receive json instead by adding the string:
# #   WANT_JSON
# # Somewhere in the file.
# # Modules can also take free-form arguments instead of key-value or json
# # but this is not recommended.
#
# arguments = shlex.split(args_data)
#
# date = str(datetime.datetime.now())
#
#
# module.exit_json(changed=True, something_else=12345)

# print json.dumps({
#     #"arguments" : arguments,
#     #"data" : args_data,
#     #"file" : args_file,
#     "time" : date,
#     "changed" : False
# })

# if __name__ == '__main__':
#     main()

#
# print json.dumps({
#     #"arguments" : arguments,
#     #"data" : args_data,
#     #"file" : args_file,
#     "time" : date,
#     "changed" : False
# })
#
