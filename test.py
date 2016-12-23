#from subprocess import call
#print call(["ulimit"]).read()
import subprocess
import re
commands = {
    #Network checks
    "network": {"commands": [
        {"command": "sysctl net.core.rmem_max","contains": "=\s?16777216$"},
        {"command": "sysctl net.core.wmem_max","contains": "=\s?16777216$"},
        {"command": "sysctl net.core.rmem_default","contains": "=\s?16777216$"},
        {"command": "sysctl net.core.wmem_default","contains": "=\s?16777216$"},
        {"command": "sysctl net.core.optmem_max","contains": "=\s?40960$"},
        {"command": "sysctl net.ipv4.tcp_rmem","contains": "=\s?4096\s87380\s16777216$"},
        {"command": "sysctl net.ipv4.tcp_wmem","contains": "=\s?4096\s87380\s16777216$"},
        {"command": "sysctl vm.max_map_count","contains": "=\s?1048575$"},
        {"command": "sysctl net.ipv4.tcp_moderate_rcvbuf","contains": "=\s?1$"},
        {"command": "sysctl net.ipv4.tcp_no_metrics_save","contains": "=\s?1$"},
        {"command": "sysctl net.ipv4.tcp_mtu_probing","contains": "=\s?1$"},
        {"command": "sysctl net.core.default_qdisc","contains": "=\s?fq$"}
    ]},
    #Memory checks
    "memory": {"commands": [
        {"command": "sysctl vm.min_free_kbytes","contains": "=\s?1048576$"},
        {"command": "sysctl vm.dirty_background_ratio","contains": "=\s?5$"},
        {"command": "sysctl vm.dirty_ratio","contains": "=\s?10$"},
        {"command": "sysctl vm.zone_reclaim_mode","contains": "=\s?0$"},
        {"command": "sysctl vm.swappiness","contains": "=\s1$"},
        {"command": "free", "contains": "Swap:\s*0\s*0\s*0"},
        {"command": "cat /sys/kernel/mm/transparent_hugepage/defrag", "contains": "\[never\]"},
        {"command": "cat /sys/kernel/mm/transparent_hugepage/enabled", "contains": "\[never\]"}
    ]},
    #SSD checks
   "ssd": {
       "vars": [{"disk": "sda1"}], #"vars": [{"disk": "sda1"}, {"disk": "sda2"}],
       "commands": [
        {"command": "fdisk -l /dev/{disk}","contains": "I/O size (minimum/optimal): 4096 bytes / 4096 bytes"},
        {"command": "cat /sys/block/{disk}/queue/scheduler","contains": "\[deadline\]"},
        {"command": "cat /sys/class/block/{disk}/queue/rotational","equals": "0"},
        {"command": "cat /sys/class/block/{disk}/queue/read_ahead_kb","equals": "8"}
    ]},
    #limits checks
    "ulimits": {"commands": [
        {"command": 'su cassandra -c "ulimit -l',"equals": "unlimited"},
        {"command": 'su cassandra -c "ulimit -n',"equals": "100000"},
        {"command": 'su cassandra -c "ulimit -u',"equals": "32768"},
        {"command": 'su cassandra -c "ulimit -m',"equals": "unlimited"}
    ]}}


def clean(line):
    if line.endswith('\n'):
        return line[:-1]
    return line

results = {}

for group_name, config  in commands.items():
    vars = [{}] if "vars" not in config else config["vars"]
    results[group_name] = []
    for var in vars:
        for command in config["commands"]:
            command_name  = command["command"].format(**var)
            p = subprocess.Popen(command_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = p.stdout.readlines()
            command_return = clean("".join(lines))
            result = {"command": command_name, "value": command_return}
            if "equals" in command:
                result.update({"type": "equals", "expected": command["equals"]})
                result["state"] = "error" if command_return != command["equals"] else "success"
            elif "contains" in command:
                result.update({"type": "contains", "expected": command["contains"]})
                regexp = re.compile(r''+command["contains"])
                result["state"] = "error" if regexp.search(command_return) is None else "success"
            results[group_name].append(result)

for k, values in results.items():
    print k
    for v in values:
        print v