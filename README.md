# api
La API de información de trampas SNMP permite obtener notificaciones enviadas por dispositivos de red a sistemas de gestión. No existe una API estándar, pero servicios como Azure Monitor y LogicMonitor ofrecen acceso a estos datos vía API REST. Además, bibliotecas como Net-SNMP y SNMP4J ayudan a procesar trampas, aunque no son APIs web.
# Proyecto SNMP CRUD

Este proyecto captura traps SNMP de routers Cisco (c7200, C3725, etc.), los almacena y permite gestionarlos vía API REST y una interfaz web responsiva.

## Componentes
- **Backend:** Flask + pysnmp para CRUD y escucha de traps.
- **Frontend:** HTML + Bootstrap para visualización y gestión.
- **Postman:** Colección para probar la API.

## Instalación
```bash
cd backend
pip install -r requirements.txt
python app.py
API REST
GET /api/traps → Lista todas las traps.

POST /api/traps → Agrega trap manualmente.

PUT /api/traps/<id> → Actualiza trap.

DELETE /api/traps/<id> → Elimina trap.

Postman
Importa el archivo postman/SNMP_CRUD.postman_collection.json.

SNMP en Cisco
Ejemplo en router:

pgsql
Copiar
Editar
snmp-server community public RO
snmp-server host 192.168.100.3 public
snmp-server enable traps
