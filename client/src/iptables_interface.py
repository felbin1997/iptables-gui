import re
import ipaddress
from Exceptions import *
from iptables_commands import *

class IPv4:
    ####################
    # A Class to manage iptables IPv4 Rules
    ####################
    POSSIBLE_CHAINS = ["INPUT", "FORWARD", "OUTPUT"]

    @staticmethod
    def read_v4_table(chain=None):
        ipv4_rules = []
        ipv4tables = {}

        chain = chain.upper()

        if chain not in IPv4.POSSIBLE_CHAINS:
            return False, "Chain not found!"

        if chain is None:
            for chain in IPv4.POSSIBLE_CHAINS:
                ipv4tables[chain] = IPv4.read_v4_table(chain.upper())
            return ipv4tables
        else:
            result, error = run_iptables_command("list_rules", chain=chain)
            ipv4tables[chain] = result
            
            if error:
                return False, error
            pattern = r"^\d+.*"
            for chain, v4_table in ipv4tables.items():
                match = re.findall(pattern, v4_table, re.MULTILINE)
                for rule in match:
                    ipv4_rules.append(IPv4.extract_v4_line_data(rule, chain))

        return ipv4_rules

    @staticmethod
    def extract_v4_line_data(v4_line, chain):
        # Zerlege die ersten Spalten mit fester Breite
        parts = v4_line.split(maxsplit=10)  # First 9 columns are fixed width, the rest is the rest of the line        
        # Dictionary with all data
        rule_dict = {
            "num": int(parts[0]),
            "pkts": int(parts[1]),
            "bytes": parts[2],
            "target": parts[3],
            "protocol": parts[4],
            "opt": parts[5],
            "in": parts[6],
            "out": parts[7],
            "source": parts[8],
            "destination": parts[9],
            "chain": chain
        }
        extra_info = parts[10:] if len(parts) > 10 else []
        
        # Optional: Protocol extraction
        if extra_info:
            extra_str = " ".join(extra_info)
            match = re.search(r"(\w+)\s+dpt:(\d+)", extra_str)
            if match:
                rule_dict["protocol"] = match.group(1)  # z. B. "tcp"
                rule_dict["port"] = int(match.group(2))  # z. B. 22
        
        return rule_dict


    @staticmethod
    def add_v4_rule(source, destination, protocol, chain, target, port=None, IN=None, OUT=None):
        chain = chain.upper()  # Chains are always uppercase

        if IN == "*":
            IN = None
        if OUT == "*":
            OUT = None
        
        # Test if the IP is a valid Address
        try:
            ipaddress.ip_network(source, strict=False)
            ipaddress.ip_network(destination, strict=False)
        except ValueError as e:
            return False, f"Ungültige IP-Adresse: {e}"

        # Selection of the right command
        if chain == "INPUT" and IN:
            command_key = "add_rule_input_interface"
        elif chain == "OUTPUT" and OUT:
            command_key = "add_rule_output_interface"
        elif chain == "FORWARD" and OUT or IN:
            command_key = "add_rule_forward_interface"
        else:
            command_key = "add_rule"

        if command_key not in IPTABLES_IPV4_COMMANDS:
            return False, f"Fehler: Unbekannter iptables-Befehl {command_key}"

        try:
        # Creates a IPTables Command with all parameters
            success, error = run_iptables_command(
                command_key,
                chain=chain,
                protocol=protocol,
                source=source,
                destination=destination,
                port=str(port) if port else "",
                target=target,
                IN=IN if IN else "",
                OUT=OUT if OUT else ""
            )
        except Exception as e:
            return False, e.args
        return success, error

    @staticmethod
    def delete_v4_rule(chain, line_number):
        command_key = "delete_rule_line_number"
        chain = chain.upper()
        try:
            success, error = run_iptables_command(
                command_key=command_key,
                chain = chain,
                line_number = line_number
            )
        except Exception as e:
            return False, e.args
        
        return success, error


    @staticmethod
    def change_v4_rule(chain, line_number, attributes):
        ipv4rules = IPv4.read_v4_table(chain.upper())
        for eintrag in ipv4rules: 
            if eintrag["num"] == int(line_number):
                suchergebnis = eintrag

        try:
            if suchergebnis:
                suchergebnis.update({key: attributes.get(key, suchergebnis[key]) for key in suchergebnis})
            else:
                raise Exception
        except Exception as e:
            return False, e.args
        
        success, error = IPv4.delete_v4_rule(chain, line_number)
        if success == False:
            return False, error
        
        ## Delete all fields that aren't needed to write a rule
        suchergebnis.pop('num', None)
        suchergebnis.pop('pkts', None)
        suchergebnis.pop('bytes', None)
        suchergebnis.pop('opt', None) # Delete options -- Need to add the ability to add these to rules
        suchergebnis.pop('in', None)
        suchergebnis.pop('out', None)
        suchergebnis['chain'] = chain
        # write the rule to iptables

        success, error = IPv4.add_v4_rule(**suchergebnis)

        return True, error