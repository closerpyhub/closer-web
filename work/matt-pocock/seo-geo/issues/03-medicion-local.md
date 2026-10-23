# 03 · Preparar medición y consentimiento en el sitio

Status: needs-info
Blocked by: E03/E04: ID autorizado de GA4 y aviso de privacidad factual completo

## Entrega

Instrumentación local comprobada que conserva contacto/cotizador y mide sólo acciones permitidas cuando existe configuración y aceptación.

## Pasos

1. Leer medicion.md completo y arquitectura.md.
2. Implementar función única de eventos en script.js, mapeos cerrados y disparos del contrato.
3. Implementar carga condicional de GA4 y estado de consentimiento básico. Sin ID, dejarlo desactivado.
4. Añadir preferencias accesibles y privacidad.html con hechos comprobados. Si faltan datos del aviso, conservar borrador fuera de raíz y código desactivado, sin ID/banner/enlaces inexistentes; probar el flujo habilitado con fixture privado completo. Completar datos humanos antes de activar.
5. Aplicar enlaces compartidos y hash de recursos. Añadir privacidad al conjunto requerido y sitemap cuando sea una página final completa.
6. Probar en navegador con destino interceptado: consentimiento, payload, ausencia de PII, duplicados y fallos.
7. Ejecutar regresión de contacto/cotizador y validación de paquete.

## Aceptación

- [ ] Contrato de cinco eventos de aplicación, incluida página consentida; eventos intrínsecos del proveedor observados y saneados.
- [ ] Cero carga/emisión nueva antes de aceptar o sin configuración.
- [ ] No captura formulario/href/query/importe ni se declara un lead desde clic.
- [ ] Preferencias, rechazo/revocación y storage bloqueado comprobados.
- [ ] Flujos actuales funcionan con analítica ausente/fallida.
- [ ] Privacidad completa; o bloqueo explícito con código desactivado y sin página/enlace/banner incompletos en la salida pública.

## Registro de ejecución

23/10/2026 · No se agregó un cargador, banner ni página de privacidad incompleta: falta la propiedad autorizada, su ID público y los hechos finales del aviso. Cloudflare Web Analytics existente se conserva sin cambios. El contacto y cotizador siguen funcionando sin analítica adicional; `node --check script.js` pasó. Para activar este ticket se requieren E03/E04 y la autorización indicada en 04.
