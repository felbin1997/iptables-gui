from flask import Flask, jsonify, request
import asyncio
from flask_cors import CORS

from iptables_interface import IPv4
import threading
from receiver import Receiver
from broadcaster import Broadcaster
from rule_saver import iptabels_saver

import json


app = Flask(__name__)
CORS(app)

basepath = '/api/v1'



###### v4Filter Endpoints ######
@app.route(f'{basepath}/v4filter/<chain>' , methods=['GET'])
def get_v4_filters(chain):
    return jsonify(IPv4.read_v4_table(chain))

@app.route(f'{basepath}/v4filter/<chain>', methods=["OPTIONS"])
def answer_options(chain):
    return jsonify({"status": True})

@app.route(f'{basepath}/v4filter/<chain>', methods=['PUT'])
def add_v4_filter(chain):
    try:    
        source = request.json.get('source')
        destination = request.json.get('destination')
        protocol = request.json.get('protocol')
        port = request.json.get('port')
        target = request.json.get('target')
    except Exception as e:
        return jsonify({"Status": False, "Error": e.args})
    status, error = IPv4.add_v4_rule(source=source, destination=destination, protocol=protocol, chain=chain, port=port, target=target)
    if error:
        return jsonify({"status": status, "error": error})
    return jsonify({"status": status})

@app.route(f'{basepath}/v4filter/<chain>/<filter_line>', methods=['POST'])
def change_v4_filter(chain, filter_line):
    data = request.get_json()

    status, error = IPv4.change_v4_rule(chain, filter_line, data)

    if error:
        return jsonify({"status": status, "error": error})
    return jsonify({"status": status})

@app.route(f'{basepath}/v4filter/<chain>/<filter_line>', methods=['DELETE'])
def delete_v4_filter(chain, filter_line):
    status, error = IPv4.delete_v4_rule(chain, filter_line)

    if error:
        return jsonify({"status": status, "error": error})
    return jsonify({"status": status})

###### Filter Rule save Enpoints ########
@app.route(f'{basepath}/save/v4filters', methods=['POST'])
def save_v4_rules():
    status, error = iptabels_saver.save_current_v4_rules()
    return jsonify({"status": status, "error": error})

@app.route(f'{basepath}/load/v4filters', methods=['POST'])
def load_v4_rules():
    status, error = iptabels_saver.load_iptables_from_json()
    return jsonify({"status": status, "error": error})


###### Neighbours Endpoint ######
@app.route(f'{basepath}/neighbours', methods=['GET'])
def get_neighbours():
    filename = "data/neighbours.json"

    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            print(f"Nachbar-Daten erfolgreich aus {filename} geladen.")

            neighbours = []

            for entry in data["ips"]:
                neighbours.append(entry)

            return jsonify({"status": True, "data": neighbours})  
    except Exception as e:
        return jsonify({"status": False, "error": e.args})



#####################################
###### Starter Functions ############
#####################################

if __name__ == '__main__':
    Broadcaster.broadcast_ip()

    listener_thread = threading.Thread(target=Receiver.listen_for_broadcast, daemon=True)
    listener_thread.start()

    print(f" Errors in adding IP: {Receiver.receive_ips(Broadcaster.get_own_ip())}")
    print(f" Errors in loading Rules: {iptabels_saver.load_iptables_from_json()}")

    print("Starting Flask App.....")
    app.run(host='0.0.0.0', port=8001, debug=True)