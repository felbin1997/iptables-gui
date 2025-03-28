from iptables_interface import IPv4
import json

class iptabels_saver:
    ####################
    # A Class to save and load iptables IPv4 Rules
    ####################


    filename = "data/ipv4rules.json" # Save-Path for the v4 Rules

    @staticmethod
    def save_current_v4_rules():
        try:
            rules = IPv4.read_v4_table()
            if rules is not None:
                with open(iptabels_saver.filename, "w", encoding="utf-8") as json_file:
                    json.dump(rules, json_file, indent=4)
                return True, iptabels_saver.filename
            else:
                return False, "No rules found!"
        except Exception as e:
            return False, f"Error saving iptables rules to JSON: {e}"
        

    @staticmethod
    def load_iptables_from_json():
        try:
            with open(iptabels_saver.filename, "r", encoding="utf-8") as json_file:
                rules = json.load(json_file)
                print(f"iptables-Regeln erfolgreich aus {iptabels_saver.filename} geladen.")

                for chain, rule_list in rules.items():  # Über alle Ketten iterieren
                    for rule in rule_list:  # Jede Regel innerhalb der Kette verarbeiten
                        success, message = IPv4.add_v4_rule(
                            source=rule.get("source", "0.0.0.0/0"),
                            destination=rule.get("destination", "0.0.0.0/0"),
                            protocol=rule.get("protocol", "all"),
                            chain=chain, 
                            target=rule.get("target", "ACCEPT"),
                            port=rule.get("port", None),
                            IN=rule.get("IN", None) if rule.get("IN", "").startswith("i") else None,
                            OUT=rule.get("OUT", None) if rule.get("OUT", "").startswith("o") else None
                        )

        except FileNotFoundError:
            print(f"Fehler: Datei {iptabels_saver.filename} nicht gefunden.")
        except json.JSONDecodeError:
            print(f"Fehler: Datei {iptabels_saver.filename} enthält ungültiges JSON-Format.")
        except Exception as e:
            print(f"Unerwarteter Fehler beim Laden von {iptabels_saver.filename}: {e}")

        return False, "error" 