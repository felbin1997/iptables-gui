import subprocess
from Exceptions import *

def general():
    version = "iptables -V"
    enabled_on_boot = "chkconfig --list iptables"

def read():
    read_v4_rules = "iptables -L -v -n"

IPTABLES_IPV4_COMMANDS = {
    "add_rule_input_interface": ["iptables", "-A", "{chain}", "-p", "{protocol}", "-s", "{source}", "-d", "{destination}","-i", "{out_in}", "-j", "{target}"],
    "add_rule_output_interface": ["iptables", "-A", "{chain}", "-p", "{protocol}", "-s", "{source}", "-d", "{destination}","-o", "{out_in}", "-j", "{target}"],
    "add_rule_forward_interface": ["iptables", "-A", "{chain}", "-p", "{protocol}", "-s", "{source}", "-d", "{destination}","-i", "{out_in}", "-j", "{target}"],
    "add_rule": ["iptables", "-A", "{chain}", "-p", "{protocol}", "-s", "{source}", "-d", "{destination}", "-j", "{target}"],
    "delete_rule_complete": ["iptables", "-D", "{chain}", "-p", "{protocol}", "-s", "{source}", "-d", "{destination}", "-j", "{target}"],
    "delete_rule_line_number": ["iptables", "-D", "{chain}", "{line_number}"],
    "list_rules_chain": ["iptables", "-L", "{chain}","-v", "-n", "--line-numbers"],
    "list_rules": ["iptables", "-L", "{chain}","-v", "-n", "--line-numbers"],
    "flush_rules": ["iptables", "-F", "{chain}"],
    "check_rule": ["iptables", "-C", "{chain}", "-p", "{protocol}", "-s", "{source}", "-d", "{destination}", "-j", "{target}"]
}




def run_iptables_command(command_key, **kwargs):
    """
    Führt einen iptables-Befehl aus, basierend auf vordefinierten Befehlen in IPTABLES_COMMANDS.

    :param command_key: Der Schlüssel für den gewünschten Befehl (z. B. "add_rule").
    :param kwargs: Dynamische Werte für den Befehl (z. B. chain, source, destination, etc.).
    :return: Tuple (bool, str) -> Erfolg oder Fehlernachricht.
    """
    if command_key not in IPTABLES_IPV4_COMMANDS:
        return False, f"Unbekannter Befehl: {command_key}"

    # Befehlsvorlage aus der Datei holen und Platzhalter ersetzen
    command = [part.format(**kwargs) for part in IPTABLES_IPV4_COMMANDS[command_key]]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if isinstance(result, str):
            return result, None 
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        raise IptablesError(command, error_message)

