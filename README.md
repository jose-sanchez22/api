# Proyecto de Automatización de IRD

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
