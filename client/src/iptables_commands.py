def general():
    version = "iptables -V"
    enabled_on_boot = "chkconfig --list iptables"

def read():
    read_v4_rules = "iptables -L -v -n"