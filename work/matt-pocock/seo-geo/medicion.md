# Contrato de medición y análisis

Consultar para tickets 02–04 y 20. Es una decisión de implementación prevista, no una integración ya activa.

## Fuentes y verdad de cada indicador

| Fuente | Qué acredita | Qué no acredita por sí sola |
| --- | --- | --- |
| Search Console de https://closer.com.py/ | Consultas, impresiones, clics, cobertura y datos disponibles | Usuarios identificados, mensajes o ventas |
| Bing Webmaster Tools | Rastreo, indexación y rendimiento de su cobertura | Todo el mercado de búsqueda |
| Bing AI Performance, si está disponible | Citas/páginas/consultas en experiencias cubiertas | Ranking universal de IA ni citas de todos los asistentes |
| Cloudflare Web Analytics existente | Tráfico/experiencia dentro de su cobertura | Contactos comerciales confirmados |
| GA4 autorizado | Acciones de visitantes con consentimiento y medición operativa | Todas las visitas ni envío efectivo de WhatsApp |
| Registro comercial autorizado | Contactos, oportunidades y ventas que realmente registra | Origen exacto de cada contacto si no se conoce |
| Panel manual de preguntas GEO | Respuestas y fuentes observadas en esa muestra/fecha | Participación universal ni resultado estable garantizado |

Search Console ya fue verificada el 21/09/2026 según README. Releer datos actuales; no crear otra propiedad ni sustituir su verificación. Acceder sólo al sitio correcto con sesión autorizada. Si no hay acceso, solicitar exportaciones de los informes concretos y seguir tareas locales.

## Línea base del ticket 02

1. Fecha de extracción y zona declaradas. En GSC, conservar la zona que informa la plataforma; no convertir fechas agregadas como si fueran timestamps.
2. Exportar últimos 28 días completos disponibles y los 28 anteriores, misma propiedad/filtros. Anotar demora y fechas efectivas.
3. Consultas y páginas: clics, impresiones, CTR y posición media. Separar búsquedas de marca (“Closer”, “CloserAI” y variantes comprobadas) de no marca; guardar la regla usada.
4. Filtrar Paraguay y todos los países en tablas separadas; móvil/escritorio por separado cuando aporte. No sumar impresiones de consultas a páginas como si fueran conjuntos disjuntos.
5. Exportar estado de indexación y revisar páginas comerciales prioritarias con Inspección de URLs. Sitemap descubierto no equivale a URL indexada.
6. Obtener Bing y Cloudflare para ventanas/filtros comparables si existen accesos. Si un informe no existe o está vacío, registrar qué se observó sin inferir cero demanda.
7. Investigar las consultas candidatas de las seis guías: datos de GSC, preguntas de clientes autorizadas y resultados públicos observados con fecha/país. No exigir herramientas pagas. Volumen ausente = desconocido.
8. Mantener los seis temas y su orden por defecto. Adelantar una guía sólo si hay evidencia concreta de demanda/negocio y registrar la razón. Si dos URLs cubren la misma intención, ampliar la existente y conservar el ticket como esa entrega; no crear una duplicación.
   En esa excepción, registrar la URL elegida y propagarla al mapa de arquitectura, enlaces de contenido.md, Recursos, sitemap y clasificación del checker. No crear la ruta descartada. Una página que conserva naturaleza comercial sigue como Service con OG website; no se transforma en Article sólo para cumplir una cantidad.
9. Tomar la muestra GEO de evidencia-y-seguimiento.md antes de cambiar el sitio.

## Instrumentación prevista

Destino elegido: GA4 mediante gtag.js directo, sin GTM, píxeles de publicidad, Google Signals, user_id ni seguimiento entre dominios. Reutilizar una propiedad correcta existente si está autorizada. Si no existe: el humano habilita/autoriza su creación y suministra el ID público G-…; no pedir claves privadas.

La propiedad no es necesaria para preparar y probar código con destino interceptado. Sin propiedad/autorización, el ticket 03 puede quedar listo localmente; el 04 permanece needs-info. No introducir un ID de ejemplo que parezca operativo.

Configuración pública: atributo data-ga4-id del elemento html, presente sólo con ID real autorizado. Si falta o no valida el formato esperado, la medición adicional queda desactivada, no se muestra un banner inútil y los flujos funcionan. Es el único punto de configuración del HTML; mantenerlo consistente en todas las páginas mediante la edición mecánica correspondiente.

La lógica vive en script.js; estilos en styles.css. No añadir servicio de ingestión propio.

Referencia de implementación: [eventos con gtag.js](https://developers.google.com/analytics/devguides/collection/ga4/events). Aplicar el contrato y consentimiento de este documento al usar la API; el ejemplo genérico del proveedor no sustituye estas restricciones.

## Consentimiento y privacidad

Esta es la elección de producto del plan; no constituye una afirmación de cumplimiento legal universal.

- Modalidad básica: gtag.js y solicitudes GA4 se cargan sólo después de aceptar. Rechazo/sin elección = ninguna solicitud de la medición nueva, ni pings sin cookies.
- Orden del cargador: preparar defaults locales de consentimiento denegado sin cargar proveedor; al aceptar, actualizar sólo analytics_storage=granted. Conservar ad_storage, ad_user_data y ad_personalization=denied, Signals/personalización desactivados y send_page_view=false. Poner estos valores antes de cualquier config/inicialización del proveedor, cargar la librería y emitir una sola página saneada. No asociar “aceptar medición” a consentimiento publicitario.
- Banner no modal, accesible por teclado: “Podemos usar medición adicional para entender qué contenidos y acciones ayudan a quienes visitan la web. Podés aceptarla o continuar sin ella.” Botones con igual claridad: “Aceptar medición” y “Continuar sin medición”; enlace a privacidad.html.
- En el pie: “Preferencias de medición”. Permite cambiar/rechazar sin impedir acceso al sitio.
- Estado local mínimo: granted o denied, versión y vencimiento a 90 días. Es una elección técnica revisable, no plazo legal atribuido. Si localStorage falla, respetar elección en memoria para esa página y volver a estado no elegido en navegación siguiente.
- Al retirar: bloquear nuevos eventos, limpiar cola local y cookies GA accesibles del sitio que se hubieran creado, actualizar preferencia y reiniciar el documento de forma controlada para descargar el proveedor. No afirmar que borra datos históricos del servidor. Mantener el rechazo después de recargar.
- Escuchar storage para aplicar el retiro también en otras pestañas abiertas; una pestaña con el proveedor cargado debe bloquear/reiniciar su medición al recibir rechazo o eliminación de la preferencia. Probar explícitamente dos pestañas; no limitar revocación al manejador del botón actual.
- Privacidad describe sólo hechos activos: formulario preparado en el dispositivo; apertura voluntaria de WhatsApp; servicios externos existentes; datos analíticos previstos, consentimiento y contacto. Revisar con el responsable datos organizativos, condiciones/retención y derechos aplicables antes de activar. No copiar un aviso legal que afirme garantías no verificadas.
- Si el aviso no puede completarse, conservar su borrador fuera de la raíz y entregar la medición desactivada: sin ID, banner ni enlaces a una página inexistente. 04 queda bloqueado hasta completar el aviso. Ese estado no bloquea publicar otras mejoras.
- Mantener Cloudflare Web Analytics existente. El rechazo de esta medición adicional no puede presentarse como rechazo de toda solicitud de Cloudflare o eliminación de sus datos. Describir el alcance por separado.

## Eventos: contrato cerrado

| Evento | Disparo | Parámetros adicionales |
| --- | --- | --- |
| page_view | Una vez al iniciar medición en la página consentida | Sólo datos de página saneados |
| quote_start | Primera interacción humana con un control del cotizador, una vez por carga | service=gestion-redes; placement=quote |
| contact_prepare | Formulario válido y vista previa construida | service del select normalizado; placement=contact_form |
| whatsapp_click | Activación real de enlace WhatsApp | service y placement controlados |
| email_click | Activación real de enlace mailto | placement controlado |

Estos son cinco eventos controlados por la aplicación. GA4 puede generar eventos intrínsecos como first_visit, session_start o user_engagement; desactivar medición mejorada no garantiza su ausencia. Todo evento del proveedor debe respetar ubicación/referrer saneados y las restricciones de consentimiento. Registrar su comportamiento real en la prueba del colector.

Parámetro común page_path: ruta canónica conocida de la página, sin query ni hash. Los servicios son: gestion-redes, meta-ads, google-ads, chatbots-ia, paginas-web, apps-sistemas, campanias-creativas, automatizaciones-bi, multiple, unknown. Mapear las opciones del formulario a esos tokens; no copiar texto arbitrario.

placement permitido: header, footer, hero, body, contact_form, quote. Asignar por atributos data-* explícitos; no extraer texto/href del enlace como dimensión. Si falta, body. No añadir parámetros fuera de esta tabla.

## Reglas de emisión

1. Función única para construir/sanear/enviar eventos. Vocabulario permitido; rechazar eventos o parámetros desconocidos. La función falla sin romper navegación.
2. No poner quote_start dentro de updateTotal(): también se ejecuta al cargar y reiniciar. Escuchar una interacción real sobre un control y marcar inicio una vez por carga.
3. contact_prepare ocurre después de reportValidity y de preparar correctamente la vista previa. Una segunda preparación deliberada puede emitir otra acción; un mismo submit no puede duplicarse por dos listeners.
4. whatsapp_click se registra por activación, incluso en enlace cuyo href se genera después. Un único manejador delegado permite mouse/teclado sin duplicar click + pointer.
5. El enlace continúa su comportamiento sin esperar a la analítica. Las pruebas interceptan navegación; nunca envían el mensaje.
6. Sin aceptación previa se descartan eventos, no se almacenan ni reenvían al aceptar. Al aceptar se mide la página actual, no el historial previo.
7. Desactivar en el flujo GA4 la medición mejorada automática de formularios, clics salientes, búsquedas y otros eventos que dupliquen o capturen URLs. Desactivar envío automático de page_view y emitirlo una sola vez saneado.
8. Configurar page_location con canonical sin query/hash y page_referrer saneado como origen externo; si es interno, ruta canónica conocida o vacío. No conservar paths externos ni queries. Asegurar que la configuración rige también eventos posteriores.
9. No pasar UTM arbitrarios. Primera versión conserva atribución disponible por referrer saneado y registra su limitación. Si luego se desean campañas etiquetadas, requieren taxonomía de valores aprobados y comprobación de que ningún dato personal llega al proveedor.
10. No leer ni enviar nombre, teléfono, email, empresa, mensaje, previsualización, URL WhatsApp completa, text=, correo destinatario, números de cuenta, precio del presupuesto ni contenido libre.
11. No emitir generate_lead, purchase, venta ni “mensaje enviado” desde un clic o preparación. Si el humano quiere marcar whatsapp_click como evento clave, su nombre/definición siguen siendo clic de salida.

## Activación autorizada del ticket 04

1. Verificar organización, propiedad y flujo correctos, ID y alcance autorizado.
2. Presentar cambios externos concretos: medición mejorada desactivada, señales/publicidad desactivadas y retención propuesta mínima disponible adecuada al informe (preferir 2 meses para datos de eventos/usuarios si la propiedad lo permite). Confirmar que la configuración elegida no sobrescribe una política vigente; si existe otra, respetarla y registrar.
3. Realizar cambios externos sólo con autorización expresa para esa configuración. Añadir ID al sitio local.
4. Probar payload y consentimiento con endpoints interceptados antes de producción. No contaminar informes con datos de personas reales.
5. Después de publicar la implementación autorizada, observar los eventos de prueba identificados en la propiedad correcta, usando mecanismo de debug disponible y documentando cómo se excluyen del informe.
6. Crear dimensiones personalizadas sólo para service y placement si hacen falta; no duplicar métricas automáticas ni crear dimensiones de alta cardinalidad.
7. Releer configuración persistida. Sólo entonces declarar medición activa. Sin acceso, dejar configuración/código listos y evidencia de limitación.

## Registro comercial y fórmulas

Conservar el CRM/registro existente si lo hay. No crear una integración o CRM por este encargo. Solicitar al responsable un agregado por período con contactos recibidos, oportunidades calificadas, ventas y origen conocido; no volcar personas a Git.

- Contacto: consulta efectivamente recibida; deduplicación acordada por oportunidad/contacto en el registro privado.
- Oportunidad: necesidad compatible con servicio, responsable/canal de seguimiento y estado comercial registrados. Si el negocio usa otra definición, conservarla y explicitarla.
- Venta: confirmación real en el sistema comercial; no sólo presupuesto enviado.
- CTR = clics / impresiones de la misma fuente y filtros.
- Tasa de acciones por sesión = sesiones elegibles con al menos una acción / sesiones elegibles, si la herramienta permite deduplicarlas. Si sólo hay eventos totales, mostrar eventos y no llamar “tasa de usuarios” a su cociente.
- Costo por contacto de pauta = inversión de pauta / contactos atribuibles del mismo alcance. Costo total añade gestión si se declara.
- Conversión comercial = oportunidades únicas de la cohorte que tuvieron al menos una venta dentro de la ventana / oportunidades únicas de esa cohorte. Cada oportunidad cuenta una vez; transacciones totales van aparte. Si faltan atribución o denominador, informar no calculable.

GA4, GSC y Cloudflare tienen coberturas, consentimiento, zonas y métodos distintos; no exigir que sus totales coincidan ni sumar sus sesiones.
