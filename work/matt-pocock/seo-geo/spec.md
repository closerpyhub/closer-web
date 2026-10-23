# Especificación: crecimiento orgánico y búsqueda con IA de Closer

Status: ready-for-agent
Blocked by: None
Versión: 1 · 23/10/2026

## Problema

La web presenta los servicios y posee metadatos, canonical, sitemap, rastreo permitido y datos estructurados. La experiencia de la agencia se muestra principalmente mediante descripciones y logos. No hay en la evidencia consultada una línea base actual de consultas orgánicas, leads atribuibles, citas en IA o rendimiento real de usuarios.

El visitante necesita comprobar que Closer entiende su problema, evaluar alternativas y costos y saber qué entregar para comenzar. El negocio necesita conocer qué contenido atrae oportunidades y qué acciones terminan en conversaciones y ventas.

## Solución

Desarrollar un conjunto editorial conectado con los servicios, demostrar trabajos reales, reforzar la identidad de la agencia y medir el recorrido de descubrimiento a consulta. Conservar la arquitectura estática y la oferta comercial vigente.

El programa combina entregables que el agente puede preparar localmente con comprobaciones que dependen de cuentas, evidencias del negocio y permisos. Tener código listo no equivale a medición activa, publicación ni éxito comercial.

## Historias de usuario

1. Como visitante, quiero identificar la empresa, su experiencia y cómo contactarla.
2. Como comprador de gestión de redes, quiero distinguir honorarios, producción, pauta y adicionales.
3. Como comprador de chatbot, quiero separar implementación, mensualidad y consumo variable.
4. Como anunciante, quiero comparar Meta y Google según intención y operación.
5. Como comprador de web, quiero elegir entre landing, institucional y tienda.
6. Como responsable de atención, quiero preparar información, derivaciones y requisitos antes de implementar un chatbot.
7. Como responsable comercial, quiero distinguir clic, conversación, oportunidad y venta.
8. Como visitante, quiero conocer un trabajo concreto y sus resultados con contexto.
9. Como visitante móvil o de teclado, quiero consultar contenido y contactos sin obstáculos.
10. Como visitante, quiero elegir si acepto la medición adicional y poder cambiar esa elección.
11. Como buscador, necesito contenido visible y enlaces que se puedan rastrear.
12. Como sistema de búsqueda con IA, necesito identificar la fuente y los hechos que sustenta.
13. Como administrador, quiero saber qué URLs están indexadas, qué consultas reciben y qué oportunidades generan.
14. Como administrador, quiero conservar datos comerciales privados fuera de la web y Git.
15. Como administrador, quiero que la publicación mantenga el destino y la trazabilidad existentes.
16. Como agente ejecutor, quiero instrucciones y criterios de cierre observables para cada entrega.
17. Como administrador, quiero revisar las tendencias por períodos comparables sin confundir muestras con resultados universales.

## Decisiones de implementación

- Mantener HTML estático, contenido accesible sin JavaScript y componentes visuales existentes.
- Añadir seis guías, una página institucional y un índice de recursos. La página de privacidad se añade al preparar la medición adicional. Añadir tres casos sólo cuando sus fichas estén completas y autorizadas.
- El autor editorial inicial es la organización. Las personas, perfiles y revisores se incorporan cuando exista evidencia. Las fechas describen actos editoriales reales.
- Las guías tienen una intención distinta de la página comercial a la que enlazan. La guía explica una decisión; la ficha comercial presenta el servicio y la contratación.
- Publicar precios propios sólo si coinciden con las fuentes comerciales verificadas. Mantener explícitas unidad, periodicidad, inclusiones, exclusiones e impuestos que consten. No transformar ofertas distintas en equivalentes.
- Mantener la identidad única de la organización, el sitio y sus páginas. Los artículos añaden una entidad editorial vinculada a la página; las páginas auxiliares no pasan a ser servicios.
- Reusar las herramientas de comprobación y exportación. Extender sus reglas sólo para representar los nuevos tipos de página; conservar sus controles.
- Preparar instrumentación mínima para acciones comerciales, con parámetros de vocabulario cerrado, sin contenido de formularios ni enlaces WhatsApp completos.
- Usar GA4 como destino previsto de eventos si el usuario autoriza una propiedad. Activación con consentimiento básico, configuración pública no secreta y desactivación completa cuando falta configuración o el visitante rechaza.
- Conservar la analítica de Cloudflare existente. Documentar sus diferencias de cobertura frente a GA4 y los registros comerciales.
- Rastrear rendimiento y citas por fecha, dispositivo/motor y alcance de la fuente. Las pruebas manuales de IA son una muestra.
- Usar ventanas comparables de 28 días, con revisiones a 7/28/56/84 días desde la publicación efectiva.
- Ejecutar acciones en cuentas externas y publicación sólo dentro de permisos explícitos. Los pasos sin permiso se preparan y quedan listos para intervención humana.

## Decisiones de pruebas

La superficie principal de verificación es la página/recorrido que recibe el visitante y el paquete que realmente se publicaría.

- Mantener comprobación de enlaces, títulos, descripciones, H1, canonical, OG, JSON-LD, sitemap y rastreo.
- Añadir pruebas con Python estándar para reglas editoriales y exclusión de archivos privados del paquete.
- Probar instrumentación en navegador interceptando el destino de medición: cero solicitudes antes de consentimiento, payload permitido y una emisión por acción definida.
- Verificar teclado, móvil, JavaScript bloqueado, almacenamiento bloqueado y errores del proveedor.
- Mantener los casos de regresión existentes de contacto y cotizador.
- Verificar producción por SHA y recursos exportados en ambos dominios después de una publicación autorizada.
- Separar resultados de laboratorio, datos de campo, cobertura de indexación, citas y conversiones.

## Fuera de alcance

- Prometer Top 1, citas, ventas o un porcentaje de crecimiento sin datos.
- Cambiar precios, paquetes, condiciones, moneda de referencia o productos históricos.
- Migrar hosting, crear nuevos servicios de infraestructura o modificar DNS.
- Campañas pagas, generación masiva de páginas por ciudad o artículos automáticos sin aporte.
- Comprar enlaces/reseñas o inventar resultados, certificaciones, perfiles o sedes.
- Integrar WhatsApp/CRM/backend u obtener confirmaciones de mensajes mediante seguimiento del navegador.
- Publicar contenido social o tomar decisiones de aprobación humana.
- Crear automatizaciones, contratos, tickets externos o sistemas de memoria adicionales.

## Cierre del programa

La entrega local se acepta técnicamente cuando las páginas habilitadas son completas, el paquete sólo contiene material público y pasan las pruebas. Los casos y medición pendientes se declaran por separado.

La salida productiva se acredita mediante el workflow, SHA y verificación de dominios. La indexación y resultados se evalúan después con datos reales. El programa de 84 días termina con un informe que explica cambios observados, incertidumbre y el siguiente trabajo recomendado; un resultado sin mejora también se informa.
