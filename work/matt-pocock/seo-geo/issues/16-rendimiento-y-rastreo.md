# 16 · Medir experiencia y corregir problemas observados

Status: needs-info
Blocked by: datos de campo autorizados y una medición de laboratorio comparable para rendimiento

## Entrega

Evaluación reproducible de rendimiento/rastreo y correcciones locales justificadas.

## Pasos

1. Seguir validacion-publicacion.md: páginas representativas, móvil/escritorio, campo vs laboratorio.
2. Capturar baseline público de rutas ya existentes y anotar disponibilidad de CrUX. Medir nuevas páginas/cambios locales con laboratorio sobre preview; PSI del dominio actual no prueba una modificación local.
3. Corregir sólo causas verificadas dentro de este sitio; preservar legibilidad, contacto y consentimiento.
4. Repetir medición comparable y regresiones de las páginas afectadas.
5. Comprobar robots/canonical/sitemap y acceso mediante herramientas autorizadas.
6. Documentar límites de verificación de bots/WAF sin ampliar permisos.

## Aceptación

- [ ] Datos de campo y laboratorio identificados y no mezclados.
- [ ] LCP/INP/CLS informados con período/dispositivo cuando existen.
- [ ] Cambios tienen antes/después y pruebas funcionales.
- [ ] Sin datos de campo no se declara aprobada esa métrica.
- [ ] Bloqueos externos precisos y controles de hosting intactos.

La ausencia de datos públicos de páginas aún no publicadas no bloquea 17. Después de 18, repetir comprobación pública y esperar muestra de campo cuando corresponda; conservar el seguimiento sin fabricar resultados.

## Registro de ejecución

23/10/2026 · Vista previa local: portada/guía de redes a 320 px y Recursos a 390 px sin desbordamiento (`scrollWidth = clientWidth`), con un H1 por página y cero errores/advertencias de consola. Esto es comprobación funcional local, no un dato de campo ni una medición comparable de LCP/INP/CLS. No se modificó rendimiento sin cuello observado. Pendiente: baseline público autorizado y tres pasadas de laboratorio comparables; repetir en producción tras 18.
