

class MethodNotImplementedError(Exception):
    def __init__(self):
        super().__init__("This Method is not implemented yet")




class IptablesError(Exception):
    IPTABLES_ERRORS = {
        "No chain/target/match by that name": "Die angegebene Kette, das Ziel oder das Match-Modul existiert nicht.",
        "Permission denied": "Fehlende Berechtigung. Führe das Skript mit sudo aus.",
        "iptables: Bad rule": "Die Regel ist fehlerhaft formatiert oder ungültig.",
        "Couldn't load match": "Das angeforderte iptables-Modul fehlt oder ist nicht geladen.",
        "Invalid argument": "Falsches Argument oder ungültige Option in der Regel.",
        "Table does not exist": "Die angegebene Tabelle existiert nicht. Stelle sicher, dass du 'filter', 'nat' oder 'mangle' nutzt."
    }


    def __init__(self, command, error_message):
        self.command = " ".join(command)  # Der ausgeführte iptables-Befehl als String
        self.raw_message = error_message  # Originale Fehlermeldung
        self.friendly_message = self._get_friendly_message(self.IPTABLES_ERRORS)
        super().__init__(self.friendly_message)

    def _get_friendly_message(self, known_errors):
        """
        Looks for known errors in the error message and returns a friendly message.
        """
        for known_error, explanation in known_errors.items():
            if known_error in self.raw_message:
                return f"{explanation} (Befehl: {self.command})"
        
        return f"Unbekannter Fehler bei iptables: {self.raw_message} (Befehl: {self.command})"

    def __str__(self):
        return self.friendly_message