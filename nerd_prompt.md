# Prompt para nerd.lat

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
