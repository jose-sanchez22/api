import os

# Estructura de directorios
dirs = ['configs', 'database', 'src', 'web', 'topology']
files = {
    '.gitignore': '''# Archivos de Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
*.egg

# Bases de datos locales
*.db
*.sqlite3

# Archivos de GNS3 generados
*.gns3project
*.gns3p

# Archivos de sistema y editores
.DS_Store
*.swp
*.swo
.vscode/
.idea/

# Archivos de caché y temporales
*.log
*.cache
*.tmp

# Archivos sensibles
*.env
*.key
*.pem
''',
    'README.md': '''# Proyecto de Automatización de IRD

Este proyecto implementa un sistema de automatización de red para monitorear trampas SNMP utilizando una API REST, configurado en una topología de GNS3 con routers Cisco c7200, switches, servidores y PCs. La API REST se implementa con Flask y pysnmp, utiliza una base de datos Supabase para almacenar trampas SNMP, y se propone una interfaz web generada con nerd.lat.

## Estructura del Proyecto
- **configs/**: Configuraciones de los routers R1, R2, R3.
- **database/**: Esquema SQL para Supabase.
- **src/**: Código Python con la API REST.
- **web/**: Prompt para la interfaz web en nerd.lat.
- **topology/**: Archivo de topología GNS3 y captura de pantalla.
- **requirements.txt**: Dependencias de Python.

## Requisitos
- GNS3 con imágenes IOS c7200.
- Ubuntu Server con Python 3.8+.
- Supabase para la base de datos.
- Postman para probar la API.
- Acceso a nerd.lat para la interfaz web.

## Configuración
1. **Topología GNS3**:
   - Importa `topology/topology.gns3` en GNS3.
   - Carga las configuraciones de `configs/` en los routers (R1, R2, R3).
   - Asegúrate de que ubuntu-server-1 esté en la red 192.168.100.0/24.
2. **Base de datos**:
   - Crea un proyecto en Supabase.
   - Ejecuta `database/tables.sql` en el SQL Editor de Supabase.
3. **API REST**:
   - Instala dependencias: `pip install -r requirements.txt`.
   - Configura las credenciales de Supabase en `src/app.py`.
   - Ejecuta el servidor: `python src/app.py`.
4. **Pruebas**:
   - Usa Postman para probar los endpoints en `http://192.168.100.10:5000`.
   - Endpoints: `GET /traps`, `GET /traps/<id>`, `POST /traps`, `PUT /traps/<id>`, `DELETE /traps/<id>`.
5. **Interfaz web**:
   - Usa `web/nerd_prompt.md` en nerd.lat para generar la interfaz.
   - Despliega la interfaz en un servidor web (e.g., Apache/Nginx en ubuntu-server-1).

## Topología
- **R1**: Conecta a NAT1 (10.0.1.0/30), R2 (10.0.0.0/30), R3 (10.0.2.0/30), ESW1 (192.168.100.0/24). DHCP para ESW1.
- **R2**: Conecta a R1, ESW1, ESW2 (192.168.10.0/24). DHCP para ESW2.
- **R3**: Conecta a R1, ESW3 (172.16.0.0/24), Cloud1. DHCP para ESW3.
- **Servidores**: ubuntu-server-1 (API REST, 192.168.100.10), UbuntuDockerGuest-1.
- **Switches**: ESW1, ESW2, ESW3 conectan servidores y PCs.

## Configuración de Routers
- Carga `R1_config.txt`, `R2_config.txt`, `R3_config.txt` en los routers.
- Verifica conectividad con `ping` y trampas SNMP al servidor (192.168.100.10).

## Ejecución
1. Inicia la topología en GNS3.
2. Configura el servidor Ubuntu con la API REST.
3. Prueba los endpoints con Postman.
4. Genera la interfaz web con nerd.lat.

## Licencia
MIT
''',
    'configs/R1_config.txt': '''hostname R1
enable secret cisco123
!
interface GigabitEthernet1/0
 ip address 10.0.1.1 255.255.255.252
 description Conexión a NAT1
 no shutdown
!
interface Serial4/0
 ip address 10.0.0.1 255.255.255.252
 description Conexión a R2
 clock rate 64000
 no shutdown
!
interface Serial4/1
 ip address 10.0.2.1 255.255.255.252
 description Conexión a R3
 clock rate 64000
 no shutdown
!
interface Serial4/1.10
 encapsulation dot1Q 10
 ip address 192.168.100.1 255.255.255.0
 description Conexión a ESW1
 no shutdown
!
ip dhcp pool LAN-ESW1
 network 192.168.100.0 255.255.255.0
 default-router 192.168.100.1
 dns-server 8.8.8.8
 lease 0 8
!
ip dhcp excluded-address 192.168.100.1 192.168.100.10
!
snmp-server community public RO
snmp-server host 192.168.100.10 version 2c public
snmp-server enable traps
!
ip route 0.0.0.0 0.0.0.0 10.0.1.2
!
line vty 0 4
 password cisco
 login
!
end
''',
    'configs/R2_config.txt': '''hostname R2
enable secret cisco123
!
interface Serial4/0
 ip address 10.0.0.2 255.255.255.252
 description Conexión a R1
 no shutdown
!
interface GigabitEthernet1/0
 ip address 192.168.10.1 255.255.255.0
 description Conexión a ESW2
 no shutdown
!
interface GigabitEthernet2/0
 ip address 192.168.100.2 255.255.255.0
 description Conexión a ESW1
 no shutdown
!
ip dhcp pool LAN-ESW2
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
 lease 0 8
!
ip dhcp excluded-address 192.168.10.1 192.168.10.10
!
snmp-server community public RO
snmp-server host 192.168.100.10 version 2c public
snmp-server enable traps
!
ip route 0.0.0.0 0.0.0.0 192.168.100.1
!
line vty 0 4
 password cisco
 login
!
end
''',
    'configs/R3_config.txt': '''hostname R3
enable secret cisco123
!
interface Serial4/0
 ip address 10.0.2.2 255.255.255.252
 description Conexión a R1
 no shutdown
!
interface GigabitEthernet1/0
 ip address 172.16.0.1 255.255.255.0
 description Conexión a ESW3
 no shutdown
!
interface FastEthernet0/0
 ip address 172.16.0.2 255.255.255.0
 description Conexión a Cloud1
 no shutdown
!
ip dhcp pool LAN-ESW3
 network 172.16.0.0 255.255.255.0
 default-router 172.16.0.1
 dns-server 8.8.8.8
 lease 0 8
!
ip dhcp excluded-address 172.16.0.1 172.16.0.10
!
snmp-server community public RO
snmp-server host 192.168.100.10 version 2c public
snmp-server enable traps
!
ip route 0.0.0.0 0.0.0.0 10.0.2.1
!
line vty 0 4
 password cisco
 login
!
end
''',
    'database/tables.sql': '''-- Tabla para almacenar trampas SNMP
CREATE TABLE traps (
    id SERIAL PRIMARY KEY,
    oid VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla opcional para usuarios (si necesitas autenticación manual)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''',
    'src/app.py': '''from flask import Flask, request, jsonify
from supabase import create_client, Client
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import threading
import os

app = Flask(__name__)

# Configuración de Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-supabase-key')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Receptor de trampas SNMP
def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    trap_info = {}
    for name, val in varBinds:
        trap_info[str(name)] = str(val)
    supabase.table('traps').insert({
        'oid': trap_info.get('1.3.6.1.2.1.1.3.0', 'unknown'),
        'message': 'Trap received'
    }).execute()

snmpEngine = engine.SnmpEngine()
config.addTransport(snmpEngine, udp.domainName, udp.UdpTransport().openServerMode(('0.0.0.0', 162)))
config.addV1System(snmpEngine, 'my-area', 'public')
ntfrcv.NotificationReceiver(snmpEngine, cbFun)
threading.Thread(target=snmpEngine.transportDispatcher.runDispatcher, daemon=True).start()

# Endpoints de la API REST
@app.route('/traps', methods=['GET'])
def get_traps():
    response = supabase.table('traps').select('*').execute()
    return jsonify(response.data)

@app.route('/traps/<int:id>', methods=['GET'])
def get_trap(id):
    response = supabase.table('traps').select('*').eq('id', id).execute()
    if response.data:
        return jsonify(response.data[0])
    return jsonify({'error': 'Trap not found'}), 404

@app.route('/traps', methods=['POST'])
def create_trap():
    data = request.get_json()
    response = supabase.table('traps').insert({
        'oid': data.get('oid', ''),
        'message': data.get('message', '')
    }).execute()
    return jsonify({'message': 'Trap created'}), 201

@app.route('/traps/<int:id>', methods=['PUT'])
def update_trap(id):
    data = request.get_json()
    response = supabase.table('traps').update({
        'oid': data.get('oid', ''),
        'message': data.get('message', '')
    }).eq('id', id).execute()
    if response.data:
        return jsonify({'message': 'Trap updated'})
    return jsonify({'error': 'Trap not found'}), 404

@app.route('/traps/<int:id>', methods=['DELETE'])
def delete_trap(id):
    response = supabase.table('traps').delete().eq('id', id).execute()
    if response.data:
        return jsonify({'message': 'Trap deleted'})
    return jsonify({'error': 'Trap not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
''',
    'web/nerd_prompt.md': '''# Prompt para nerd.lat

Crea una interfaz web responsiva para gestionar datos de trampas SNMP en una red privada. La interfaz debe interactuar con una API REST en http://192.168.100.10:5000. Los endpoints son:

- GET /traps: Lista todas las trampas
- GET /traps/<id>: Detalles de una trampa por ID
- POST /traps: Crear trampa (JSON: { "oid": "", "message": "" })
- PUT /traps/<id>: Actualizar trampa (JSON: { "oid": "", "message": "" })
- DELETE /traps/<id>: Eliminar trampa

**Características**:
1. **Autenticación**: Página de login con usuario/contraseña y logout.
2. **Panel de control**: Resumen (número total de trampas).
3. **Gestión de trampas**:
   - Página para listar trampas con opciones para ver, editar o eliminar.
   - Página para agregar trampa.
   - Página para ver/editar trampa específica.
4. **Manejo de errores**: Mensajes para errores (trampa no encontrada, problemas de red).
5. **Diseño**: Limpio, profesional, con menú de navegación. Responsivo para desktop y móvil.
6. **Técnico**: Usa JavaScript (Fetch/Axios) para llamadas API. Incluye HTML, CSS, JavaScript.
7. **Despliegue**: Instrucciones para servidor local (Apache/Nginx en Ubuntu). Uso en red privada.

**Seguridad**: Autenticación robusta para acceso no autorizado. Prioriza funcionalidad y usabilidad.
''',
    'requirements.txt': '''flask==2.3.2
pysnmp==4.4.12
supabase==2.7.1
'''
}

# Crear directorios
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Crear archivos
for file_path, content in files.items():
    with open(file_path, 'w') as f:
        f.write(content)

print("Estructura de directorios y archivos creada. Asegúrate de añadir topology.gns3 y topology.png en el directorio topology/")