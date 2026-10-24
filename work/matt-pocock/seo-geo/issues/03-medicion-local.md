# 03 · Preparar medición directa en el sitio

Status: done
Blocked by: ninguno

## Entrega

Instrumentación local comprobada que conserva contacto/cotizador y mide sólo acciones permitidas cuando existe configuración.

## Pasos

1. Leer medicion.md completo y arquitectura.md.
2. Implementar función única de eventos en script.js, mapeos cerrados y disparos del contrato.
3. Implementar carga automática de GA4. Sin ID, dejarla desactivada; mantener almacenamiento/publicidad de Google bloqueados fuera de la analítica necesaria.
4. Añadir privacidad.html con hechos comprobados, sin preferencias ni banner. Completar datos humanos antes de activar.
5. Aplicar enlaces compartidos y hash de recursos. Añadir privacidad al conjunto requerido y sitemap cuando sea una página final completa.
6. Probar en navegador con destino interceptado: carga automática, payload, ausencia de PII, duplicados y fallos.
7. Ejecutar regresión de contacto/cotizador y validación de paquete.

## Aceptación

- [x] Contrato de cinco eventos de aplicación, incluida página automática; eventos intrínsecos del proveedor observados y saneados.
- [x] GA4 carga automáticamente cuando existe configuración; sin ID no hay carga ni emisión.
- [x] No captura formulario/href/query/importe ni se declara un lead desde clic.
- [x] No hay banner, preferencias, rechazo ni revocación en el sitio; la parte publicitaria de Google permanece bloqueada.
- [x] Flujos actuales funcionan con analítica ausente/fallida.
- [x] Privacidad completa; o bloqueo explícito con código desactivado y sin página/enlace/banner incompletos en la salida pública.

## Registro de ejecución

23/10/2026 · No se agregó un cargador, banner ni página de privacidad incompleta: falta la propiedad autorizada, su ID público y los hechos finales del aviso. Cloudflare Web Analytics existente se conserva sin cambios. El contacto y cotizador siguen funcionando sin analítica adicional; `node --check script.js` pasó. Para activar este ticket se requieren E03/E04 y la autorización indicada en 04.

23/10/2026 · Se creó la propiedad GA4 autorizada y se incorporó su ID público real mediante `data-ga4-id` en las páginas. El cargador directo de `script.js` permanece sin proveedor antes de la aceptación; conserva publicidad/Signals desactivados, `send_page_view: false`, preferencia local versionada de 90 días y revocación que limpia cookies accesibles y reinicia el documento. La instrumentación sólo permite `page_view`, `quote_start`, `contact_prepare`, `whatsapp_click` y `email_click`, con rutas, servicios y ubicaciones controladas. La vista previa comprobó ausencia de script/cola antes de elegir; luego interceptó la etiqueta para comprobar el único `page_view` saneado y la revocación, sin enviar datos a Google. Falta observar recepción desde la versión publicada.

23/10/2026 · La comprobación de recepción autorizada se hizo después del despliegue publicado. Una visita técnica consentida, sin formulario ni datos personales, cargó la etiqueta `G-16GG9X2PR5`; la tarjeta de tiempo real de la propiedad correcta mostró 1 usuario activo desde Paraguay. La instrumentación local y la recepción real quedan distinguidas: la primera controló consentimiento, payload y revocación; la segunda confirmó que la versión pública llega a GA4.

24/10/2026 · El responsable autorizó sustituir la carga condicionada por carga automática de GA4 sin banner ni preferencias en el sitio. La instrumentación mantiene los cinco eventos cerrados, la exclusión de PII, la medición mejorada/Signals/personalización publicitaria desactivados y `send_page_view=false`; cambian únicamente el momento de carga y la eliminación de los controles de consentimiento. La verificación de esta versión debe comprobar carga automática, payload saneado y ausencia del banner.
