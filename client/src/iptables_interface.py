import subprocess
import re
import ipaddress

#from iptables_commands import general

def list_iptables_rules():
    try:
        try: 
            command = ["sudo"]
        except Exeption as e: 
            print("You might have no root rights: ")
            print(e)

        #ans = subprocess.check_output(["iptables", "-L", "-v", "-n"],shell=True, text=True)
        try:
            version = read_version()
            ipv4_rules = read_v4_table("INPUT")
            #first_rule = extract_v4_line_data(ipv4_rules[0])

            print(ipv4_rules)

        except Exception as e:
            print("probably no iptables installed:") 
            print(e)


        #systemctl list-units --type=service --state=active
        #ans = subprocess.check_output(["systemctl", "list-units", "--type=service", "--state=active"] ,shell=True, text=True)




    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")




def read_version():
    version_string = subprocess.check_output(["iptables", "-V"], text=True)
    version_string = version_string[version_string.find('v')+1:]
    version_string = version_string[:version_string.find(' ')]

    return version_string

def read_v4_table(chain=None):

    ipv4_rules = []

    if chain is None:
        v4_table = subprocess.check_output(["iptables", "-L", "-v", "-n", "--line-numbers"], text=True)
    else:
        v4_table = subprocess.check_output(["iptables", "-L",chain , "-v", "-n", "--line-numbers"], text=True)

    pattern = r"^\d+.*"
    match = re.findall(pattern, v4_table, re.MULTILINE)

    for rule in match:
        ipv4_rules.append(extract_v4_line_data(rule))

    return ipv4_rules


def extract_v4_line_data(v4_line):
    # Zerlege die ersten Spalten mit fester Breite
    parts = v4_line.split(maxsplit=10)  # Die ersten 9 Spalten fest aufteilen
    
    # Dictionary mit den extrahierten Daten
    rule_dict = {
        "num": int(parts[0]),
        "pkts": int(parts[1]),
        "bytes": parts[2],  # Bytes bleibt als String (weil es K/M/G haben kann)
        "target": parts[3],
        "protocol": parts[4],
        "opt": parts[5],
        "in": parts[6],
        "out": parts[7],
        "source": parts[8],
        "destination": parts[9]
    }
    
    # Falls die Zeile weitere Infos enthält (z. B. "tcp dpt:22"), extrahiere sie
    extra_info = parts[10:] if len(parts) > 10 else []
    
    # Optional: Versuche, Protokoll-Optionen zu extrahieren (z. B. "tcp dpt:22")
    if extra_info:
        extra_str = " ".join(extra_info)
        match = re.search(r"(\w+)\s+dpt:(\d+)", extra_str)
        if match:
            rule_dict["extra_protocol"] = match.group(1)  # z. B. "tcp"
            rule_dict["destination_port"] = int(match.group(2))  # z. B. 22
    
    return rule_dict


if __name__ == "__main__":
    list_iptables_rules()