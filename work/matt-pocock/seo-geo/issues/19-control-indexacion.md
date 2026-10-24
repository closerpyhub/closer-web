# 19 · Verificar descubrimiento e indexación posteriores

Status: needs-info
Blocked by: revisión D+7 por URL pendiente

## Entrega

Estado de nuevas URLs y cualquier causa concreta que impida su inclusión.

## Pasos

1. Comprobar sitemap público, canonical y robots de nuevas páginas.
2. En GSC/Bing autorizados, leer estado de las URLs y canonical seleccionado. Registrar fecha/fuente.
3. Solicitar indexación o cambiar envíos sólo si hay autorización externa específica.
4. Revisar en D+7. Si hay demoras sin error, mantener observación; si hay causa comprobada, preparar corrección local.
5. No usar búsquedas site: como inventario completo ni cambiar noindex histórico.

## Aceptación

- [ ] Cada URL nueva tiene estado/fuente/fecha o falta de acceso explícita.
- [ ] Descubierta/rastreada/indexada se distinguen.
- [ ] Causas técnicas observadas corregidas localmente y revalidadas.
- [ ] Acciones externas y publicación de correcciones tienen su autorización.

Un control correcto puede cerrar aunque un buscador tarde; la indexación no observada conserva un pendiente con criterio y fecha de nueva revisión, sin prometerla.

## Registro de ejecución

23/10/2026 · Control técnico de D0 completado para las ocho URLs nuevas: el sitemap público contiene las 28 URLs de la versión, `robots.txt` conserva la política fuente junto a la política administrada de Cloudflare y ambos dominios sirven el HTML marcado con el SHA `f1ea30c`. Las pruebas locales del mismo SHA validaron canonical, metadata, grafo JSON-LD y enlaces de las páginas. Esto prueba publicación y rastreabilidad técnica, no descubrimiento, rastreo ni indexación por buscadores.

24/10/2026 · Ya hay lectura autorizada en ambas propiedades. Search Console aún sólo expone el agregado de 3 páginas indexadas y 18 no indexadas; Bing confirma el sitemap importado sin errores, con 28 URLs descubiertas, pero indica que sus informes siguen procesándose. No se solicitó indexación ni se cambió un envío externo. La revisión D+7 por URL permanece el 30/10/2026: distinguirá descubierta, rastreada e indexada con la fuente y fecha de cada URL prioritaria.
