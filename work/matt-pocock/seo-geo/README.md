# Guía de ejecución SEO y GEO de WEB Closer

Fecha de diseño: 23/10/2026 · Zona: America/Asuncion.
Status: ready-for-agent

## Empezar aquí

Este paquete convierte el diagnóstico del chat en trabajo ejecutable. El encargo que lo produjo autoriza crear esta guía; todavía no ejecuta sus cambios en el sitio ni autoriza publicar. Cuando el usuario encargue su ejecución, aplicar la secuencia siguiente.

El resultado buscado es una web con pruebas de experiencia, contenido útil, identidad verificable y medición de consultas comerciales y citas. El proyecto tiene una base técnica válida. Alcanzar primeras posiciones o ser citado por una IA depende de terceros y no es un criterio de cierre que el agente pueda garantizar.

### Mensaje para entregar al agente ejecutor

> Ejecutá la guía work/matt-pocock/seo-geo/README.md de este repositorio. Leé sus reglas y trabajá ticket por ticket sobre la frontera disponible. Autorizo preparar e implementar localmente los cambios descritos y verificarlos. Usá las decisiones, estructuras y textos del paquete; completá datos mediante fuentes verificables. Si falta un dato humano, registrá el bloqueo concreto y continuá con los tickets independientes. Entregá una vista previa y evidencia de validación. Los commits, pushes, publicación, configuración de cuentas y mensajes externos necesitan su autorización específica; este mensaje no los incluye. No inventes clientes, resultados, precios, permisos, perfiles ni accesos.

### Lectura por tarea

1. Leer AGENTS.md y README.md de la raíz, este archivo y [spec.md](spec.md).
2. Leer [arquitectura.md](arquitectura.md) antes de tocar HTML, CSS, JS o herramientas.
3. Leer [contenido.md](contenido.md) al ejecutar los tickets editoriales 06–14.
4. Leer [medicion.md](medicion.md) al ejecutar 02–04 o revisar resultados.
5. Leer [evidencia-y-seguimiento.md](evidencia-y-seguimiento.md) al recopilar datos, preparar casos o ejecutar 15/19/20.
6. Leer [validacion-publicacion.md](validacion-publicacion.md) para cerrar cada cambio y antes de cualquier entrega/publicación.
7. Abrir solamente el ticket que se va a ejecutar y las evidencias que ese ticket necesita. No hace falta cargar todos los tickets en cada sesión.

Las instrucciones de este paquete son específicas del estado observado. Si el código o el alcance cambiaron, contrastar la diferencia antes de actuar; conservar los cambios ajenos.

## Decisiones ya tomadas

- Mantener sitio estático: HTML plano en la raíz, CSS y JS compartidos, Python estándar para validación/exportación. Sin migración, CMS, backend, paquete SEO ni framework nuevo.
- Primera salida editorial: seis guías definidas aquí, Sobre Closer, un índice de recursos y hasta tres casos con evidencia y permiso. Los casos no disponibles quedan pendientes; no bloquean las guías.
- Las primeras cuatro guías cubren presupuesto de redes, presupuesto de chatbot, comparación de canales y elección de web. Las dos siguientes cubren preparación de un chatbot y medición de consultas. Son hipótesis comerciales priorizadas, no palabras clave con demanda ya demostrada.
- Autor institucional inicial: Closer. Las personas y credenciales sólo se incorporan si están verificadas. La fecha editorial refleja la revisión/publicación real.
- Mantener precios/alcances existentes. Los artículos de precio se basan en la oferta de Closer y no presentan un estudio de precios de todo Paraguay.
- Reutilizar Cloudflare Web Analytics para su medición actual. Para eventos comerciales, preparar GA4 con consentimiento básico y sin publicidad; activarlo sólo con propiedad e instrucciones autorizadas. Esta elección técnica está detallada en medicion.md.
- La instrumentación mide acciones en el sitio. Contactos recibidos, calificación y ventas se confirman mediante el registro comercial autorizado; no se deducen de clics.
- Evaluar resultados por ventanas de 28 días desde la publicación. Los controles de los días 7, 28, 56 y 84 son hitos del plan; este documento no crea automatizaciones.

## Secuencia y dependencias

Los números son IDs estables. Un ticket está disponible cuando sus dependencias están integradas y verificadas. Un bloqueo externo afecta sólo a los entregables que lo necesitan.

| Ticket | Entrega | Blocked by |
| --- | --- | --- |
| [01](issues/01-baseline-local.md) | Estado inicial local y mapa de cambios | Ninguno |
| [02](issues/02-linea-base-buscadores.md) | Datos SEO, demanda y muestra GEO actuales | 01 |
| [05](issues/05-soporte-editorial.md) | Checker/export compatibles con páginas editoriales | 01 |
| [03](issues/03-medicion-local.md) | Eventos seguros y consentimiento probados localmente | 05 |
| [04](issues/04-activar-medicion.md) | Preparación autorizada; recepción real después de publicar | 03 + datos humanos para preparar; 18 sólo para cerrar recepción |
| [06](issues/06-sobre-closer.md) | Identidad institucional y perfiles verificados | 05 |
| [07](issues/07-guia-precio-redes.md) | Guía de presupuesto de redes | 05, 06 |
| [08](issues/08-guia-precio-chatbot.md) | Guía de presupuesto de chatbot | 05, 06 |
| [09](issues/09-guia-comparacion-ads.md) | Comparación Meta Ads / Google Ads | 05, 06 |
| [10](issues/10-guia-tipo-web.md) | Guía landing / institucional / tienda | 05, 06 |
| [11](issues/11-guia-preparar-chatbot.md) | Checklist para implementar chatbot | 05, 06 |
| [12](issues/12-guia-medir-whatsapp.md) | Guía de consultas y ventas por WhatsApp | 05, 06 |
| [13](issues/13-recursos-y-enlaces.md) | Recursos y mejoras enlazadas de servicios | 06 + al menos una guía 07–12 lista |
| [14](issues/14-tres-casos-verificados.md) | Hasta tres casos completos, comprobados uno por uno | 05, 06 + fichas y permisos |
| [15](issues/15-reputacion-local.md) | Auditoría local/externa y acciones preparadas | 01 |
| [16](issues/16-rendimiento-y-rastreo.md) | Rendimiento medido y correcciones justificadas | 03, 05, 13 |
| [17](issues/17-integracion-y-entrega.md) | Vista previa, QA y entrega de la tanda lista | 03, 06, 13, 16 |
| [18](issues/18-publicacion-autorizada.md) | Versión productiva y verificación de ambos dominios | 17 + autorización |
| [19](issues/19-control-indexacion.md) | Control de rastreo/indexación posterior | 18 |
| [20](issues/20-evaluacion-28-56-84.md) | Evaluación y siguientes cambios sustentados | 02, 18 + tiempo/datos |

El orden inicial es 01 → 05 → 03; luego 06 habilita las guías. Los IDs son estables y la tabla muestra las dependencias efectivas, no una obligación de ejecutar 03 antes de 05.

04, 14 y 15 tienen cierre independiente. 13 y 17 integran todas las páginas completas disponibles; pueden cerrar una primera tanda aunque alguna guía necesite información. La meta del programa sigue siendo seis guías. Cada guía incorporada más tarde actualiza también Recursos y sus enlaces, se valida y requiere su propia publicación autorizada. Ningún ticket pendiente se marca done por entregar una tanda parcial.

## Procedimiento por sesión

1. Comprobar repositorio y cambios actuales; leer el resultado del ticket anterior.
2. Elegir el primer ticket disponible. Registrar Status: in-progress y hora de inicio.
3. Ejecutar los pasos de ese ticket con sus documentos de referencia.
4. Hacer las pruebas indicadas; corregir regresiones propias.
5. Registrar archivos propios modificados, fuentes, pruebas observadas, salida verificable y siguiente acción en el mismo ticket. No copiar datos privados.
6. Marcar done sólo si cumple todos sus criterios. Si falta información externa: Status: needs-info; anotar el dato exacto y continuar la frontera.
7. Terminar con un resumen breve de resultados y bloqueos que necesiten al humano.

Estados disponibles: ready-for-agent, in-progress, needs-info, ready-for-human, done, wontfix. Registrar el motivo si un ticket queda wontfix; no usarlo para ocultar una falta.

## Datos que el agente no puede inventar

La ficha de evidencia incluye los campos exactos que se necesitan. Recuperarlos primero de fuentes autorizadas; pedir al humano una sola lista agrupada con lo que realmente falte:

- Acceso de lectura a la propiedad correcta de Search Console/Bing y fuentes de tráfico.
- Propiedad GA4, ID público del flujo, autorización de activación y datos reales de privacidad.
- Perfiles oficiales e identidad de personas si se desea mostrarlas.
- Tres trabajos seleccionados, pruebas de resultados y permiso de uso/publicación.
- Ficha local existente y modalidad real de atención para comprobar elegibilidad.

Ausencia de acceso significa Sin verificar. No significa cero visitas, cero enlaces, inexistencia de una ficha o ausencia de casos.

## Límites de ejecución

La preparación local no autoriza pushes a master: disparan el publicador productivo. Tampoco autoriza crear cuentas, modificar propiedades externas, solicitar reseñas, contactar aliados o clientes, enviar correos ni lanzar anuncios. Preparar primero el cambio y presentar el paso exacto al usuario cuando falte autorización.

La frontera social permanente de AGENTS.md sigue vigente: nunca aprobar, liberar, programar o publicar contenido social desde Codex, aunque este plan incluya materiales que alguien quiera reutilizar.

Cada entrega distingue: implementado localmente, verificado, pendiente de datos, autorizado/publicado y resultado observado. La aceptación humana del trabajo no se presume.
