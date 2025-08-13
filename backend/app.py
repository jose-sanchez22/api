from flask import Flask, request, jsonify
from pysnmp.entity import engine, config
from pysnmp.hlapi.asyncore import *
from threading import Thread

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

traps = []  # Almacén de traps en memoria

@app.route('/api/traps', methods=['GET'])
def list_traps():
    return jsonify(traps)

@app.route('/api/traps/<int:idx>', methods=['GET'])
def get_trap(idx):
    if idx < 0 or idx >= len(traps):
        return jsonify({'error': 'no existe'}), 404
    return jsonify(traps[idx])

@app.route('/api/traps', methods=['POST'])
def create_trap():
    data = request.json
    traps.append(data)
    return jsonify(data), 201

@app.route('/api/traps/<int:idx>', methods=['PUT'])
def update_trap(idx):
    if idx < 0 or idx >= len(traps):
        return jsonify({'error': 'no existe'}), 404
    data = request.json
    traps[idx] = data
    return jsonify(data)

@app.route('/api/traps/<int:idx>', methods=['DELETE'])
def delete_trap(idx):
    if idx < 0 or idx >= len(traps):
        return jsonify({'error': 'no existe'}), 404
    traps.pop(idx)
    return '', 204

def snmp_trap_listener():
    snmpEngine = engine.SnmpEngine()
    config.addTransport(
        snmpEngine,
        udp.domainName,
        udp.UdpTransport().openServerMode(('0.0.0.0', 162))
    )
    config.addV1System(snmpEngine, 'my-area', 'public')

    def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
        trap_data = {str(x[0]): str(x[1]) for x in varBinds}
        traps.append(trap_data)

    ntfrcv.NotificationReceiver(snmpEngine, cbFun)
    snmpEngine.transportDispatcher.jobStarted(1)
    snmpEngine.transportDispatcher.runDispatcher()

Thread(target=snmp_trap_listener, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
