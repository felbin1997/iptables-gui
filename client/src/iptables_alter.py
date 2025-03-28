import iptc
import ipaddress


class IPv4:
    @staticmethod
    def list_iptables_rules(chain_name="INPUT"):
        """ Listet die Regeln der angegebenen IPTables-Kette auf. """
        table = iptc.Table(iptc.Table.FILTER)
        chain = iptc.Chain(table, chain_name)

        rules = []
        for rule in chain.rules:
            rule_info = {
                "protocol": rule.protocol,
                "src": rule.src,
                "dst": rule.dst,
                "target": rule.target.name if rule.target else "UNKNOWN",
                "matches": [match.name for match in rule.matches],
                "ports": []
            }

            for match in rule.matches:
                if match.name == "tcp" and hasattr(match, "dport"):
                    rule_info["ports"].append(match.dport)

            rules.append(rule_info)

        return rules

    @staticmethod
    def add_v4_rule(source, destination, protocol, chain_name="INPUT", port=None, target="ACCEPT"):
        try:
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, chain_name.upper())
            rule = iptc.Rule()
            print(f" Table Name: {chain.name}")

            rule.protocol = protocol
            rule.src = source
            rule.dst = destination
            rule.target = iptc.Target(rule, target)

            if port:
                match = rule.create_match(protocol)
                match.dport = str(port)

            chain.append_rule(rule)
            table.commit()
            
            #print(chain.strerror())

            #chain.insert_rule(rule)
            return "Successfully entered", None
        except Exception as e:
            print(f"Error adding rule: {e}")
            return False, e.args
        
    def test(source, destination, protocol, chain_name="INPUT", port=None, target="ACCEPT"):
        rule = iptc.Rule()
        match = iptc.Match(rule, "mac")
        match.mac_source = "!00:11:22:33:44:55"
        rule.add_match(match)
        rule.target = iptc.Target(rule, "ACCEPT")
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        chain.insert_rule(rule)

        return True, None

    if __name__ == "__main__":
        print("Aktuelle IPTables-Regeln:")
        rules = list_iptables_rules()
        for r in rules:
            print(r)
