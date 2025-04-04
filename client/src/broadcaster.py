import socket
import time
from pydbus import SystemBus
from gi.repository import GLib

class Broadcaster:
    ###################################
    # 
    # Class for broadcasting the own IP 
    #                                 
    ###################################

    BROADCAST_IP = "255.255.255.255"
    PORT = 5005

    @staticmethod
    def get_own_ip():
        """Ermittelt die eigene IP-Adresse"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    @staticmethod
    def broadcast_ip():
        """Sendet die eigene IP per Broadcast ins Netzwerk"""
        own_ip = Broadcaster.get_own_ip()
        message = f"APP_ADDRESS:{own_ip}:8080"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), (Broadcaster.BROADCAST_IP, Broadcaster.PORT))
        sock.close()
        

    @staticmethod
    def network_changed(*args):
        Broadcaster.broadcast_ip()

