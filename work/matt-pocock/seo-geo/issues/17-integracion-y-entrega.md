# 17 · Integrar, verificar y entregar para revisión

Status: done
Blocked by: ninguno para la entrega de esta tanda; 03 y 16 permanecen con sus datos externos pendientes

## Entrega

Versión local revisable y paquete público íntegro, con pendientes explícitos.

## Pasos

1. Integrar cambios propios, todas las guías completas disponibles y casos/medición externos que ya estén listos; conservar pendientes independientes. Un precio en conflicto no bloquea entregar otras guías.
2. Ejecutar todos los comandos, recorridos y casos de validacion-publicacion.md.
3. Inspeccionar cada archivo del export y revisar diff completo de la tarea.
4. Actualizar README raíz con comportamiento activo y comprobado, sin reescribir historia de despliegues.
5. Registrar mapa URL → intención → servicio → evidencia → estado.
6. Entregar vista previa, pruebas observadas y acción concreta de publicación si procede.

## Aceptación

- [ ] Todas las páginas habilitadas completas y sin placeholders.
- [ ] Metadata/grafos/sitemap/enlaces/export y regresiones pasan.
- [ ] No hay datos privados, credenciales ni borradores en el paquete.
- [ ] Casos y medición pendientes se declaran por estado real.
- [ ] Usuario tiene resultado concreto para revisar.

La meta editorial del programa es seis guías. Una tanda parcial puede cerrar 17 si se declara exactamente qué URLs contiene y qué tickets siguen pendientes; no convertirlos a done. Cada tanda posterior vuelve a aplicar 17 y requiere autorización de publicación propia.

La finalización de 17 no marca completo el programa de indexación/resultados ni autoriza 18.

## Registro de ejecución

23/10/2026 · Tanda local: `nosotros`, `recursos` y seis guías (`precio-gestion-redes-paraguay`, `precio-chatbot-whatsapp-paraguay`, `meta-ads-vs-google-ads`, `landing-page-o-web-institucional`, `preparar-chatbot-whatsapp`, `medir-consultas-whatsapp`). `check_site` pasó con 32 páginas/28 URLs; 12 pruebas Python, `node --check`, `git diff --check` y export pasaron. El export observó 54 archivos y excluyó trabajo/documentación/materiales/herramientas. Vista previa funcional: portada → guía y Recursos a 320/390 px sin desbordamiento ni errores de consola; el formulario preparó una consulta con datos sintéticos sin abrir WhatsApp ni enviar nada. Pendiente separado: analítica GA4/privacidad, baseline/rendimiento de campo, casos verificables, reputación e indexación posterior. La publicación y su control público quedaron registrados en 18.
