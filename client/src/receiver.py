import socket
import json
import time
import os

class Receiver:
    ###################################
    # Class for receiving Broadcastet #
    # Adresses of other nodes         #
    #                                 #
    ###################################
    @staticmethod
    def receive_ips(message):
        json_file = "data/neighbours.json"
        os.makedirs("data", exist_ok=True)  # Stelle sicher, dass der Ordner existiert

        try:
            # Nur weitermachen, wenn Format stimmt
            if not message.startswith("APP_ADDRESS:"):
                return False, "Unerkanntes Format"

            # IP extrahieren
            parts = message.strip().split(":")
            if len(parts) != 3:
                return False, "Ungültiges Adressformat"

            ip = parts[1]  # z.B. "10.3.0.111"

            # Bestehende Daten laden
            try:
                with open(json_file, "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {"ips": []}

            if "ips" not in data:
                data["ips"] = []

            if ip in data["ips"]:
                return False, "IP Already known"

            # IP hinzufügen und speichern
            data["ips"].append(ip)
            with open(json_file, "w") as file:
                json.dump(data, file, indent=4)

            print(f"[Receiver] Neue IP gespeichert: {ip}")
            return False, None

        except Exception as e:
            return True, str(e)
    
    
    @staticmethod
    def listen_for_broadcast(BROADCAST_PORT=5005):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", BROADCAST_PORT))

        print(f"Broadcast-Listener läuft auf Port {BROADCAST_PORT}...")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                iserror, error = Receiver.receive_ips(data.decode())
                if iserror:
                    print(f"There was an error receiving the IPs: {error}")
                else:
                    print(f"Empfangen von {addr}: {data.decode()}")
            except Exception as e:
                print(f"Fehler beim Empfang: {e}")
                time.sleep(5)

    


if __name__ == '__main__':
    print("Starte Receiver-Listener...")
    Receiver.listen_for_broadcast()




