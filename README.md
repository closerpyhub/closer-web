# Closer · Web

Sitio estático de Closer E.A.S. Se trabaja desde esta carpeta; conserva el historial del repositorio `thomasyaluff-ui/closer-web`. No requiere un framework, instalación de paquetes ni compilación.

## Ejecutar localmente

Desde PowerShell, en la raíz:

```powershell
.\tools\start-preview.ps1
```

Abrir [http://127.0.0.1:8765](http://127.0.0.1:8765). El servidor de desarrollo está limitado al equipo local. El lanzador inicia Python en segundo plano, fija esta carpeta como raíz y dirige la salida a archivos `closer-web-preview-8765.*.log` en la carpeta temporal de Windows. Comprueba que la portada responde y muestra el PID del servidor. No interrumpe procesos si el puerto ya está ocupado; se puede usar `-Port 8766` para una instancia separada.

El servidor queda independiente de la terminal temporal del agente. Esto evita repetir el fallo observado en la vista previa: un proceso seguía escuchando, pero cerraba las conexiones sin respuesta (`ERR_EMPTY_RESPONSE`), dejando páginas en caché sin estilos o JavaScript. Para detener una instancia, usar `Stop-Process -Id <PID>` con el PID informado por el lanzador.

Como alternativa, en una terminal que permanezca abierta se puede ejecutar `python -m http.server 8765 --bind 127.0.0.1` desde esta carpeta.

## Estructura

- `index.html`: portada, servicios, marcas, recorrido, acceso al cotizador y preguntas frecuentes.
- Ocho páginas de servicios y trece páginas `plan-*.html`: alcances, importes y consultas.
- `gestion-redes.html#arma-tu-plan`: cotizador de redes.
- `contacto.html`: preparación de una consulta y apertura voluntaria de WhatsApp.
- `index-opcion-servicios-clara.html`: variante histórica conservada y adaptada al diseño compartido.
- `styles.css`: identidad, componentes y comportamiento responsive de todo el sitio.
- `script.js`: navegación, cotizador y preparación de contacto.
- `assets/`: logo original, imágenes y fuentes locales. Los originales se conservan; la web utiliza versiones WebP optimizadas.
- `tools/check_site.py`: validación estática sin dependencias externas.
- `tools/start-preview.ps1`: inicio de la vista previa local con registros independientes de la terminal.
- `tools/build_site.py`: exportación filtrada de los archivos públicos para despliegue.

La navegación, el pie y los metadatos están en el HTML de cada página para funcionar sin JavaScript. Los cambios compartidos deben aplicarse a todas las páginas. Los enlaces a CSS y JS usan un parámetro `v` basado en los primeros diez caracteres del SHA-256 del archivo; actualizarlo cuando cambie el recurso evita mezclar HTML nuevo con recursos antiguos en caché.

## Contacto

El formulario valida los campos y prepara una vista previa local. Solo al pulsar «Abrir WhatsApp con mi consulta» se abre el enlace con el mensaje. El visitante confirma su envío en WhatsApp. No hay un backend de formularios ni almacenamiento, y no se presenta una confirmación de envío ficticia. Editar el formulario invalida la preparación anterior.

Sin JavaScript, la preparación queda deshabilitada y se ofrecen enlaces directos a WhatsApp y correo. El formulario no transmite datos por GET.

## Cotizador y condiciones comerciales

Los precios y las reglas originales se conservan. La base mensual de redes es Gs. 330.000; las fotos se calculan con un mínimo de cinco cuando se solicita al menos una. Las campañas incluidas se activan al agregar publicaciones. El costo variable de respuestas del bot se presenta aparte del total fijo.

La equivalencia en dólares usa la **tasa histórica del 28/05/2026**, 1 USD = Gs. 6.068,93. No se consulta una cotización actual. La pauta publicitaria y los cargos variables mantienen sus condiciones originales.

Las tres rutas históricas `plan-chatbots-atencion-inteligente.html`, `plan-chatbots-optimizacion.html` y `plan-chatbots-robot-avanzado.html` conservan precios distintos al producto principal `plan-chatbot-ia.html`. No se sustituyeron ni se asumió que sus propuestas son equivalentes. Antes de cambiar la oferta comercial, confirmar cuáles corresponden.

## Verificar

```powershell
python tools/check_site.py
node --check script.js
git diff --check
```

La comprobación estática revisa las 24 rutas, títulos, descripciones, H1, IDs, archivos locales y destinos de anclas. También valida canonical, coherencia de Open Graph, JSON-LD, política de indexación, sitemap y permisos de rastreo. No realiza solicitudes externas.

Verificación del rediseño (10/09/2026): 23 páginas en 390, 768 y 1440 px; navegación con teclado y móvil; comportamiento sin JavaScript; contacto con entradas largas; cotizador y reinicio. Sin errores de JavaScript, recursos faltantes ni desbordamiento del documento. Las pruebas no enviaron mensajes.

La corrección de marca y SEO se verificó en 23 páginas, con 35 preguntas desplegables abiertas y anchos de 320, 390, 768 y 1440 px. Se corrigieron contrastes de estados hover, campos de formulario y un desbordamiento a 320 px. Pasaron nuevamente los casos base/publicación/mínimo de fotos/IA/reinicio del cotizador, menú móvil con Escape, preparación e invalidación de contacto y navegación sin JavaScript. La validación SEO local pasó con 19 URLs indexables, 111 nodos de entidad JSON-LD y cero errores.

Casos útiles de regresión del cotizador, restableciendo el resto de los campos entre casos:

| Selección | Total Gs. | USD aproximados |
| --- | ---: | ---: |
| Base | 330.000 | 54 |
| Una publicación | 385.000 | 63 |
| Una foto (mínimo de cinco) | 550.000 | 91 |
| Seis fotos | 594.000 | 98 |
| Community con IA | 980.000 | 161 |
| Ambas opciones adicionales, IA, informe BI, 12 publicaciones, 5 fotos, 2 reels cortos, 1 video de un minuto y 1 video largo | 3.710.000 | 611 |

## Identidad y recursos

Se mantienen el logo original y la paleta de la web original: turquesa `#0098b8`, variante `#0089a6`, celestes `#dff7fc` y `#eefbfd`, blanco y tinta `#14343c`. Los archivos gráficos originales tienen un turquesa dominante cercano a `#009eba`. Los enlaces y botones usan una variante más oscura del mismo tono (`#00738c`) para mantener contraste legible. Los fondos oscuros y los verdes menta de la primera propuesta se reemplazaron por blanco y celeste. Manrope se sirve localmente; su licencia está en `assets/fonts/OFL.txt`.

La pieza activa de la portada está en `assets/brand/closer-eye-studio.png`; se entrega como `assets/brand/closer-eye-studio.webp` (1254 × 1254, 87.324 bytes). El 15/09/2026 se reemplazó la C por el ojo original de Closer con sus dos patitas, reinterpretado como una escultura de vidrio turquesa sobre blanco. Tres nodos y sus conexiones integran el símbolo con las ideas, los procesos y los datos. Las versiones anteriores se conservan como recursos de trabajo, pero no se publican ni se usan en Open Graph.

Se creó con la herramienta integrada `image_gen`, usando `logo-closer.png` como referencia de identidad y la C anterior como referencia de material e iluminación. Dirección del prompt: conservar aro circular turquesa, ojo blanco, pupila oscura a la derecha, brillo y dos patas; interpretación escultórica frontal con profundidad, suelo blanco/celeste, tres nodos conectados, bordes blancos y ningún texto, letra C o elemento de interfaz dentro de la imagen. Es una pieza conceptual de marca, no una fotografía de un trabajo para clientes.

El favicon de las 24 páginas es `assets/brand/closer-eye-icon.png` (512 × 512, transparente). Se aisló el ojo con sus patitas mediante `image_gen` tomando únicamente el logo original como referencia; el prompt pidió mantener geometría y colores, sin letras adyacentes, perspectiva ni fondo. Se revisó a 16 y 32 px. Se cambió también la URL del recurso para evitar reutilizar el favicon anterior de la caché.

Las frases de la portada son texto HTML visible y accesible: «Ideas que conectan», «Eficiencia en los procesos» y «Números que respaldan acciones». Se muestran en tres columnas en escritorio y en filas en pantallas pequeñas, con texto oscuro e iconos turquesa. El contenedor ya no usa `aria-hidden` y las frases no se ocultan en móvil.

## SEO y búsqueda con IA

El contenido comercial permanece en HTML y puede leerse sin ejecutar JavaScript. La portada identifica a Closer como agencia de marketing digital y tecnología en Paraguay, y las páginas de servicios describen alcances, requisitos, costos y preguntas frecuentes. No se añadieron cifras de resultados, reseñas, direcciones, certificaciones ni afirmaciones de liderazgo sin respaldo.

| Página principal | Intención de búsqueda cubierta |
| --- | --- |
| `index.html` | Agencia de marketing digital e inteligencia artificial en Paraguay |
| `gestion-redes.html` | Gestión de redes sociales, community manager, contenido y publicidad en redes |
| `meta-ads.html` | Agencia y gestión de Meta Ads en Paraguay, publicidad en Facebook e Instagram |
| `chatbots-ia.html` | Chatbots con IA para WhatsApp, atención, ventas, cobranzas y agendamientos |
| `paginas-web.html` | Diseño y desarrollo web, landing pages, sitios institucionales y tiendas online |
| `apps-sistemas.html` | Aplicaciones, software a medida, sistemas internos e integraciones |
| `campanias-creativas.html` | Campañas publicitarias, concepto creativo, copywriting y contenido |
| `google-ads.html` | Agencia y gestión de Google Ads, anuncios y seguimiento de campañas |
| `automatizaciones-bi.html` | Automatización de procesos, email marketing, Manychat y Business Intelligence |

Las fichas de mailing, Manychat y BI desarrollan esas soluciones concretas. `meta-ads.html` se añadió el 21/09/2026 porque la pauta en Meta solo aparecía como una mención dentro de gestión de redes, mientras las páginas que Google mostraba para consultas de agencias tenían una URL especializada. La página explica el alcance respaldado por la oferta existente, distingue gestión e inversión, responde cómo elegir una agencia y enlaza el cotizador; no afirma que Closer sea «la mejor» ni inventa resultados. Las frases describen servicios respaldados por la web y los materiales del proyecto; no representan una investigación de volúmenes de búsqueda ni posiciones medidas. Las presentaciones y el documento del asesor respaldan la actividad en Paraguay y el inicio de Closer en 2016; no se inventó una dirección física o cobertura por ciudad.

Cada página tiene título y descripción propios, canonical HTTPS, Open Graph y un grafo JSON-LD con la identidad de la organización, el sitio y la página. Cloudflare Pages redirige las rutas `.html` a direcciones sin extensión: los canonical, Open Graph, identificadores JSON-LD y sitemap usan esas direcciones públicas finales. Los enlaces internos conservan `.html` para funcionar también en la vista previa; la navegación reconoce ambos formatos. Las páginas de servicios y planes incluyen `Service`; las internas, `BreadcrumbList`. El catálogo de la portada enlaza las siete áreas. El marcado describe el contenido y no garantiza resultados enriquecidos.

`sitemap.xml` contiene 20 URLs canónicas indexables. La variante `index-opcion-servicios-clara.html` y las tres fichas históricas de chatbots llevan `noindex, follow` y se excluyen del sitemap. Conservan sus URLs, su contenido y sus precios; no se redirigen a productos con otro alcance. Antes de promover esas fichas antiguas, confirmar su vigencia comercial y actualizar tanto el sitemap como la comprobación estática.

`robots.txt` permite el rastreo de páginas y recursos públicos a través de la regla general, que incluye Googlebot, Bingbot y OAI-SearchBot. Excluye las carpetas internas `.git`, `materials`, `tools` y el README. Estas reglas no son controles de acceso: la publicación debe incluir solo archivos públicos. No se añadieron reglas específicas de entrenamiento de modelos. Ninguna página con `noindex` se bloquea al rastreo, para que el buscador pueda leer esa directiva.

La implementación sigue [las recomendaciones de Google para sus funciones con IA](https://developers.google.com/search/docs/appearance/ai-features) y [la documentación de OAI-SearchBot](https://developers.openai.com/api/docs/bots): contenido claro, enlaces accesibles y rastreo permitido. No requiere archivos especiales para IA ni instrucciones ocultas. No garantiza indexación, citas en respuestas o primeras posiciones.

### Verificación después de una publicación autorizada

Preparar el paquete público ejecutando `python tools/build_site.py`. Primero valida el sitio y después copia las 24 páginas, CSS/JS, sitemap/robots, los recursos usados y la licencia de la fuente a una carpeta temporal nueva. Imprime su ruta como `PUBLIC_SITE_DIR`. También acepta `--output` con una carpeta nueva o vacía; no borra contenido existente. El paquete contiene 46 archivos; el comando informa el peso actualizado. No subir la raíz del repositorio: incluye materiales y herramientas que no corresponden a la web pública.

La versión renovada se publicó el 10/09/2026. Se comprobó que el dominio canónico entrega las 23 páginas, `robots.txt`, `sitemap.xml` y los recursos con HTTP 200. El sitemap publicado coincide con el paquete y el robots público permite Googlebot, Bingbot y OAI-SearchBot. En Google Search Console queda pendiente verificar la propiedad si fuera necesario, enviar el sitemap e inspeccionar las URLs principales; no se accedió a esa herramienta durante este despliegue. Revisar cobertura de indexación, consultas, impresiones y clics con el tiempo. El sitio no incorpora medición de posiciones ni nuevas herramientas de analítica.

## Alojamiento y despliegue

El sitio existente está en Cloudflare Pages, proyecto `closer-web`, rama de producción `master`. Sus dominios son `closer.com.py`, `www.closer.com.py` y `closer-web.pages.dev`. La publicación puede realizarse directamente con Wrangler usando el directorio público exportado, sin cambiar DNS ni la conexión Git existente:

```powershell
python tools/build_site.py
# Usar la ruta PUBLIC_SITE_DIR que devuelve el comando anterior.
wrangler pages deploy <PUBLIC_SITE_DIR> --project-name closer-web --branch master --commit-hash <COMMIT>
```

La autenticación de Wrangler usa la sesión de Cloudflare del equipo; no se guardan credenciales en el proyecto. Si vence, renovar la sesión con `wrangler login`.

Página de Meta Ads publicada el 21/09/2026: `17e0ae0f-298f-4d40-ba1a-a2bea0c16baa`, código `5e9629a4d06739eeb51cc429007eb700c1cbac2a`, URL permanente [17e0ae0f.closer-web.pages.dev](https://17e0ae0f.closer-web.pages.dev). El paquete contiene 46 archivos (576.822 bytes). Cloudflare confirmó el entorno Production y la rama master. En el dominio canónico se comprobaron la portada, `/meta-ads`, la redirección desde `/meta-ads.html` y el sitemap con HTTP 200. Chromium móvil confirmó la navegación real desde la portada, H1, contenido completo, ausencia de desbordamiento y cero errores de consola; las únicas solicitudes no estáticas fueron dos eventos de analítica de Cloudflare con respuesta 204.

Actualización de identidad publicada el 15/09/2026: `553e84d9-aac0-43ea-96fd-5bb7c4f53663`, código `e95f7bce29c3c8fb1708069a83e74975eb5bfac6`, URL permanente [553e84d9.closer-web.pages.dev](https://553e84d9.closer-web.pages.dev). Incluye favicon del ojo, nueva portada y Open Graph, y tres frases legibles. Paquete: 45 archivos, 559.860 bytes. Pasaron 41 comprobaciones locales (siete anchuras de 320 a 1440 px, accesibilidad de frases, metadatos de 23 páginas, enlaces, cotizador y contacto). Contraste de las frases: 13,239:1. En producción se comprobaron los 45 archivos con HTTP 200 y referencias/versiones correctas; nueva imagen, favicon, frases en escritorio/móvil y acceso al cotizador confirmados en Chromium, sin errores JavaScript.

Despliegue de producción del rediseño, confirmado el 10/09/2026: `6998ba99-8397-426b-b911-0f2e9952ae5b`, código `81d6572e701268e022b331f30ba622475efd08c2`, URL permanente [6998ba99.closer-web.pages.dev](https://6998ba99.closer-web.pages.dev). Se exportaron y publicaron 45 archivos públicos (521.089 bytes). Cloudflare confirmó el entorno Production y la rama master; `closer.com.py`, `www.closer.com.py` y `closer-web.pages.dev` sirven la versión renovada.

La verificación con Chromium sobre el dominio público pasó los siete servicios desde la portada, diez fichas de planes, el cotizador, la preparación e invalidación de contacto, el menú móvil y la página activa en rutas sin extensión. No se enviaron mensajes ni se abrió WhatsApp. No hubo errores JavaScript ni respuestas HTTP de error en recursos propios; el bloqueo deliberado del beacon de analítica en el entorno de prueba se excluyó de los fallos del sitio.

El dominio personalizado conserva transformaciones de Cloudflare preexistentes: protección de enlaces de correo, el script de Web Analytics y un bloque administrado al inicio de robots.txt con restricciones para algunos rastreadores de entrenamiento. Las páginas coinciden con el paquete tras descontar esas inserciones; CSS, JavaScript y recursos coinciden byte a byte. Los enlaces de correo se restauran con el script de Cloudflare. No se modificaron DNS, configuración de rastreadores, analítica ni la conexión Git del hosting.

Versión de producción anterior al rediseño: `ad2ee419-8683-4375-8fd6-e1bfb7e71f5b`, correspondiente a `a56989e`, disponible en `https://ad2ee419.closer-web.pages.dev`. Cloudflare conserva los despliegues previos para recuperar una versión si fuera necesario.

La cuenta GitHub disponible (`closerpyhub`) tiene lectura del repositorio `thomasyaluff-ui/closer-web`, pero no permiso de push. El código nuevo está guardado en la rama local `codex/closer-web-refresh`. El despliegue directo no sincroniza GitHub: antes de disparar una futura publicación automática desde Git, subir esta versión con una cuenta que tenga escritura para evitar reponer el sitio antiguo.
