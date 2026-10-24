# Instrucciones técnicas

Consultar antes de los tickets 03 y 05–18.

## Estado observado

- HEAD inicial: 6a6a85c60df82b714dd3b474a7b8ce4b3d0b1c95; master; remoto closerpyhub/closer-web.
- 24 HTML planos; 20 URLs en sitemap; 4 páginas históricas noindex. La comprobación anterior al plan pasó con 116 nodos de grafo. Estos son datos de partida, no totales que deban seguir fijos.
- La navegación y el pie se repiten en cada HTML. No dependen de renderizado JavaScript.
- El exportador descubre todos los HTML de la raíz. No reconoce un estado borrador.
- El exportador recoge href/src relativos y url() del CSS principal. Un recurso referenciado sólo en OG o JSON-LD puede no entrar al paquete.
- El verificador actual exige un WebPage y og:type=website. SERVICE_ROUTES se deriva de REQUIRED_ROUTES; ampliar ese conjunto sin separar tipos clasificaría guías como Service.
- El hosting elimina la extensión .html; la vista previa necesita archivos .html.
- La protección de correo y Cloudflare Web Analytics se insertan en producción. No duplicarlos desde el código local.

## Archivos y rutas elegidos

| Entrega | Archivo público final | Canonical |
| --- | --- | --- |
| Institucional | nosotros.html | /nosotros |
| Recursos | recursos.html | /recursos |
| Guía redes | precio-gestion-redes-paraguay.html | /precio-gestion-redes-paraguay |
| Guía chatbot | precio-chatbot-whatsapp-paraguay.html | /precio-chatbot-whatsapp-paraguay |
| Comparación Ads | meta-ads-vs-google-ads.html | /meta-ads-vs-google-ads |
| Tipo de web | landing-page-o-web-institucional.html | /landing-page-o-web-institucional |
| Preparar chatbot | preparar-chatbot-whatsapp.html | /preparar-chatbot-whatsapp |
| Medir consultas | medir-consultas-whatsapp.html | /medir-consultas-whatsapp |
| Privacidad/analítica | privacidad.html | /privacidad |
| Casos autorizados | caso-<slug-estable>.html | /caso-<slug-estable> |

Los slugs de casos se determinan después de seleccionar el trabajo autorizado. Usar nombre público del proyecto; con autorización de anonimización, un identificador descriptivo no reidentificante. Nunca crear archivos literales con esos marcadores.

Borradores editoriales van en work/matt-pocock/seo-geo/borradores/ como Markdown; reportes públicos sin datos sensibles en el ticket correspondiente. Los HTML finales entran a la raíz sólo cuando están completos y aptos para publicación. Noindex no vuelve privado un archivo.

## Implementar una página nueva

1. Reutilizar contacto.html o una página de servicio como estructura visual; sustituir contenido, identidad de página y metadatos.
2. Mantener lang=es-PY, viewport, skip link, header/footer, defer y estilos compartidos.
3. Un solo H1 descriptivo; title y description únicos. OG coincide con title/description/canonical; imagen y alt describen la imagen real.
4. Canonical absoluto https://closer.com.py/<slug>; enlaces internos relativos a <slug>.html y anclas existentes.
5. Contenido principal en HTML: respuesta inicial, secciones, tablas accesibles, FAQ visible y CTA. No inyectarlo desde JS ni ocultarlo a personas.
6. Artículos: columna de lectura de 65–75 caracteres aproximadamente, encabezados con scroll-margin, índice por anclas si supera cinco H2, tabla adaptable sin desbordar la página. Sin rediseño global.
7. Reutilizar imagen de marca sólo como marca; no presentarla como fotografía de un trabajo real. No hace falta producir una imagen genérica por guía.
8. Si hay imagen de caso, usar src relativo visible bajo assets/cases/ con dimensiones y texto alternativo; WebP cuando corresponda, original privado fuera del paquete. Una imagen OG debe incluirse realmente en el export.
9. Añadir enlace contextual de ida y vuelta con el servicio relacionado. No enlazar artículos pendientes.
10. Añadir canonical al sitemap sólo cuando el HTML final existe e indexa. Mantener intactas las cuatro exclusiones históricas.
11. Aplicar reglas del checker y validación del paquete antes de considerar lista la página.

## JSON-LD y OG

Un script application/ld+json con @graph por página. Mantener @id de Organization y WebSite existentes.

- Guía/caso: Organization + WebSite + WebPage + BreadcrumbList + Article.
- Institucional/recursos/privacidad: Organization + WebSite + WebPage + BreadcrumbList. No hace falta multiplicar subtipos para este proyecto.
- Servicios originales: conservar Service. Los artículos se relacionan por about o menciones descriptivas; no copiar ofertas en ellos sin necesidad.
- WebPage.mainEntity referencia <canonical>#article. Article.mainEntityOfPage referencia <canonical>#webpage; author y publisher, #organization. Cada @id local referenciado tiene definición en ese grafo, conforme al checker.
- Article incluye headline, description, url y author. datePublished/dateModified sólo con fechas reales. image sólo si el recurso existe y se exporta.
- Autor visible: “Por Closer”. Enlace a nosotros.html. Personas sólo cuando verificadas; no “revisado por” sin revisión real.
- Organization.sameAs sólo perfiles oficiales verificados. Conservar nombre legal, teléfono y email existentes salvo evidencia autorizada de corrección.
- Mantener FAQ en HTML; no añadir FAQPage, Review, AggregateRating, premios ni LocalBusiness como táctica de enriquecimiento.
- og:type=article para artículos; website en el resto. No hace falta ofrecer rich results ni prometerlos.

## Cambios exactos del checker

En tools/check_site.py:

1. Separar SERVICE_ROUTES del crecimiento de REQUIRED_ROUTES mediante una lista explícita de los servicios/planes actuales. Preservar los históricos aunque sigan noindex.
2. Crear ARTICLE_ROUTES con las guías/casos realmente incorporados, no borradores previstos. Incorporar las nuevas páginas terminadas a REQUIRED_ROUTES.
3. Esperar og:type=article sólo en ARTICLE_ROUTES; website en el resto.
4. Mantener un WebPage. Exigir un Article adicional en ARTICLE_ROUTES; validar headline, author y la relación a WebPage. Rechazar Service añadido por clasificación accidental a una guía.
5. Verificar coincidencia de fechas editoriales visibles y schema cuando existan; una fecha ausente en un borrador fuera de raíz no es una fecha ficticia.
6. Mantener cálculo dinámico del sitemap y todos los controles actuales; no desactivar checks para hacer pasar una página.
7. Añadir pruebas focalizadas en tools/test_check_site.py: servicio conserva Service; artículo válido; artículo mal clasificado; OG inconsistente; sitemap faltante/noindex incluido; referencias locales rotas.

Preferir las funciones y HTMLParser existentes, Python unittest y carpetas temporales. No añadir dependencias.

## Exportación y archivos privados

Mantener tools/build_site.py como exportador único. No copiar work/, materials/, .git/, .codex/, Desechos/, originales privados o reportes por comodidad.

El plan evita nuevos JS/CSS separados: la medición vive en script.js y sus estilos en styles.css. Si por una razón concreta se separa un recurso, hay que añadirlo explícitamente al exportador y a la comprobación; no basta con enlazarlo.

Cada imagen editorial se muestra con src relativo para que el mecanismo actual la recoja. Añadir una prueba del exportador que compruebe: HTML nuevos incluidos; imagen visible incluida; documentación/borrador/reporte excluidos. No añadir _headers o _redirects sin un encargo justificado y soporte explícito en export/verificación.

## Navegación y recursos compartidos

- Añadir Sobre Closer, Recursos y Privacidad al pie compartido cuando sus páginas estén listas; desde 24/10/2026 la analítica carga automáticamente y no expone “Preferencias de medición”.
- Conservar las ocho áreas del menú y evitar sobrecargar el header móvil.
- En portada: enlace a nosotros desde “Somos Closer”; bloque pequeño “Guías para decidir” con las cuatro primeras guías; los casos autorizados se añaden junto a las marcas sin atribuir un caso a todos los logos.
- Añadir enlaces contextuales en servicios según contenido.md. Preservar contacto, cotizador y todas las rutas históricas.
- Después de editar CSS/JS, calcular SHA-256 y sustituir v en todos los HTML por sus primeros diez caracteres. Comprobar todos, no sólo portada:

~~~powershell
(Get-FileHash -Algorithm SHA256 -LiteralPath 'styles.css').Hash.ToLower().Substring(0,10)
(Get-FileHash -Algorithm SHA256 -LiteralPath 'script.js').Hash.ToLower().Substring(0,10)
~~~

No alterar el marcador closer-release de los fuentes: lo añade el exportador al preparar la versión del SHA correcto.
