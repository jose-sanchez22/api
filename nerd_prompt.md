# Prompt para nerd.lat

Crea una interfaz web responsiva para gestionar datos de trampas SNMP en una red privada. La interfaz debe interactuar con una API REST en http://192.168.100.10:5000. Los endpoints son:

- GET /traps: Lista todas las trampas
- GET /traps/<id>: Detalles de una trampa por ID
- POST /traps: Crear trampa (JSON: { "oid": "", "message": "" })
- PUT /traps/<id>: Actualizar trampa (JSON: { "oid": "", "message": "" })
- DELETE /traps/<id>: Eliminar trampa

**Caracter�sticas**:
1. **Autenticaci�n**: P�gina de login con usuario/contrase�a y logout.
2. **Panel de control**: Resumen (n�mero total de trampas).
3. **Gesti�n de trampas**:
   - P�gina para listar trampas con opciones para ver, editar o eliminar.
   - P�gina para agregar trampa.
   - P�gina para ver/editar trampa espec�fica.
4. **Manejo de errores**: Mensajes para errores (trampa no encontrada, problemas de red).
5. **Dise�o**: Limpio, profesional, con men� de navegaci�n. Responsivo para desktop y m�vil.
6. **T�cnico**: Usa JavaScript (Fetch/Axios) para llamadas API. Incluye HTML, CSS, JavaScript.
7. **Despliegue**: Instrucciones para servidor local (Apache/Nginx en Ubuntu). Uso en red privada.

**Seguridad**: Autenticaci�n robusta para acceso no autorizado. Prioriza funcionalidad y usabilidad.
