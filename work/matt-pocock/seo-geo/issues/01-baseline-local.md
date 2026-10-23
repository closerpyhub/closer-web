# 01 · Recuperar y verificar el punto de partida

Status: done
Blocked by: None

## Entrega

Estado inicial reproducible del proyecto y alcance de cambios propios, sin alterar la web.

## Pasos

1. Leer entrada, spec y validacion-publicacion.md.
2. Comprobar raíz, origin, rama, HEAD y cambios pendientes. Preservar AGENTS.md y este paquete si no están rastreados.
3. Ejecutar las comprobaciones iniciales indicadas; registrar fallas preexistentes con salida mínima.
4. Confirmar páginas, sitemap, noindex, schema, formularios y convención de export en el código actual.
5. Releer portada, robots y sitemap públicos. Registrar la versión pública observada; si no coincide, separar lo local de lo publicado.
6. Registrar las diferencias respecto del baseline del 23/10/2026 y elegir el siguiente ticket disponible.

## Aceptación

- [ ] Repositorio exacto y cambios ajenos identificados.
- [ ] Resultado observado de comprobaciones, no sólo comandos propuestos.
- [ ] Diferencias materiales resueltas o documentadas sin borrar trabajo.
- [ ] Evidencia pública distinguida del estado local.

## Registro de ejecución

23/10/2026 · HEAD inicial `6a6a85c60df82b714dd3b474a7b8ce4b3d0b1c95`, rama `master`, remoto `closerpyhub/closer-web`. Se preservaron `AGENTS.md` y `work/` sin rastrear. Baseline: `check_site` pasó con 24 páginas/20 URLs; 7 pruebas Python y `node --check script.js` pasaron. La versión pública observada en búsquedas sigue siendo la anterior; la tanda local no está publicada. Siguiente: 05.
