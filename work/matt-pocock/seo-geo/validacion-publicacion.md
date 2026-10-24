# Validación y publicación

## Antes de editar

Desde la raíz del proyecto, observar resultados:

~~~powershell
git rev-parse --show-toplevel
git remote get-url origin
git branch --show-current
git status --short
python tools/check_site.py
python -m unittest discover -s tools -p 'test_*.py'
node --check script.js
~~~

La raíz y remoto deben ser los de WEB Closer. El estado al preparar esta guía incluía AGENTS.md sin rastrear; pertenece al usuario y no se incorpora ni descarta por accidente. El paquete de planificación también puede seguir sin commit. No exigir limpieza borrando trabajo.

Si no hay solapamiento, continuar preservando cambios ajenos. Si un solapamiento impide trabajar, resolver el alcance con el usuario o usar un worktree administrado adecuado sin resetear el checkout. El plan no autoriza instalar herramientas globales.

Desechos/ ya existe. Material creado durante ejecución que quede ciertamente obsoleto se mueve allí bajo fecha y origen, sin sobrescribir. Fuentes, pruebas útiles, evidencia, documentación y entregables siguen en su lugar.

## Pruebas por cambio

~~~powershell
python tools/check_site.py
python -m unittest discover -s tools -p 'test_*.py'
node --check script.js
git diff --check
python tools/build_site.py
~~~

El último comando imprime PUBLIC_SITE_DIR. Inspeccionar el paquete real. Los totales aumentarán con las páginas; no modificar aserciones sólo para mantener 24/20/46.

Si cambió CSS/JS, comprobar que v corresponde al hash final en todos los HTML. Los tests de Python deben cubrir reglas editoriales/exportación añadidas; no probar copias de cada párrafo.

### Recorridos de navegador

Usar las herramientas de navegador disponibles; leer su skill si corresponde. Vista previa existente:

~~~powershell
.\tools\start-preview.ps1
~~~

Si el puerto está ocupado, comprobar si es la instancia correcta o usar -Port 8766. No terminar procesos ajenos. El lanzador ya usa ventana oculta.

| Prueba | Resultado necesario |
| --- | --- |
| Portada → servicio → guía → contacto | Enlaces y contenidos completos |
| Recursos y Sobre Closer | Accesibles sin depender del sitemap |
| Todas las páginas nuevas | Un H1, metadata correcta, anclas y breadcrumb reales |
| 320, 390, 768 y 1440 px | Sin desbordamiento de documento, CTA/índice/tablas utilizables |
| Teclado/menú móvil | Foco visible, Escape y navegación correctos |
| JavaScript bloqueado | Texto/enlaces disponibles y alternativas de contacto reales |
| Formulario inválido | No prepara ni emite contact_prepare |
| Formulario válido con datos sintéticos | Prepara una vez; editar invalida la vista previa |
| Salida WhatsApp/email | Interceptar navegación; no enviar mensaje |
| Analítica ausente/rechazada | Cero carga/envío nuevo GA4 y flujos operativos |
| Analítica aceptada | Sólo eventos/payload permitidos; sin duplicados |
| Revocación/almacenamiento bloqueado/dos pestañas | No reanuda medición contra la elección en ninguna pestaña |
| URL/query/href con datos sintéticos sensibles | Ninguno llega al destino analítico interceptado |
| Proveedor bloqueado o falla | No rompe formularios, cotizador o navegación |
| Consola/recursos | Sin nuevos errores propios ni archivos ausentes |

Para medición, obtener dos evidencias: primero probar la carga automática y el wrapper con cargador simulado; después probar la librería real con todas sus solicitudes de recolección interceptadas antes del envío. Bloquear colectores y destinos publicitarios, capturando payload sin enviarlo a una propiedad real. Usar query, UTM e identificadores publicitarios sintéticos para comprobar que no se filtran. Incluir eventos intrínsecos del proveedor. Luego, sólo con activación autorizada, observar registro persistido en la propiedad correcta. El stub no prueba el payload de la librería ni recepción real.

Si una herramienta necesaria no existe, documentar la limitación y preparar la comprobación equivalente disponible; no instalar una nueva herramienta opcional global sin permiso ni declarar prueba observada.

### Regresión de cotizador

Restablecer antes de cada caso y conservar condiciones históricas:

| Selección | Gs. esperados |
| --- | ---: |
| Base | 330.000 |
| Una publicación | 385.000 |
| Una foto, mínimo de cinco | 550.000 |
| Seis fotos | 594.000 |
| Community con IA | 980.000 |
| Reinicio | 330.000 |

Si la oferta cambió por instrucción autorizada posterior, actualizar expectativa con esa evidencia. Este plan por sí solo no cambia precios. Conservar también el caso combinado del README.

## Rendimiento y rastreo

1. Antes de publicar, medir campo/baseline sólo de rutas públicas existentes (portada, gestion-redes y contacto). Para nuevas guías/casos o modificaciones locales, usar laboratorio reproducible sobre preview. Repetir PSI público después de 18; esperar datos de campo si no hay muestra.
2. Usar PageSpeed/CrUX cuando haya datos. Registrar URL/fecha/dispositivo/período y si son datos de campo o laboratorio.
3. Objetivos de campo al percentil 75: LCP ≤ 2,5 s; INP ≤ 200 ms; CLS ≤ 0,1. Si no hay muestra suficiente, registrar “sin datos de campo”, nunca sustituirlo por un score de laboratorio.
4. Laboratorio: tres pasadas comparables antes/después y mediana para diagnosticar. Para una URL nueva sin versión anterior, establecer baseline local y comparar sus cambios posteriores. TBT no se informa como INP real. No perseguir puntuación 100 a costa de contenido o funcionalidad.
5. Corregir sólo cuello observado: dimensiones de imagen, peso real, prioridad de imagen LCP, trabajo JS innecesario o desplazamiento introducido por banner/recursos. Imagen principal visible no lazy; secundarias con lazy si corresponde.
6. Medir de nuevo páginas afectadas tras corregir. No rediseñar ni cambiar hosting por hipótesis.
7. Verificar HTTP/robots/canonical/sitemap/rutas y recursos públicos. Conservar noindex históricos.
8. Para demostrar acceso de bots auténticos usar herramientas de inspección o logs autorizados con verificación de identidad. Un 200 con User-Agent imitado sólo comprueba esa solicitud.
9. Cloudflare MCP es sólo lectura y tiene alcance limitado: antes de operar comprobar usuario/cuenta/zona/Pages del AGENTS.md. Si logs o WAF no están disponibles con ese permiso, Sin verificar; no ampliar scopes ni cambiar reglas.
10. Un bloqueo real de seguridad/rastreo se informa con evidencia y cambio propuesto para decisión humana.

## Cierre local para revisión humana

Entregar vista previa y resumen con:

- URLs/páginas listas y hechos que agregan.
- Comprobaciones efectivamente ejecutadas, resultados y limitaciones.
- Resultado de revisión de paquete, sin datos privados.
- Casos disponibles y faltantes por C1/C2/C3.
- Medición: preparada / configurada / activa con evidencia, según corresponda.
- Cambios externos/publicación todavía pendientes y acción concreta que necesitan.

Actualizar README.md raíz únicamente con comportamiento activo verificado, comandos y nuevas categorías. Conservar los datos fechados de despliegues históricos. El registro de ejecución vive en los tickets, sin otra memoria paralela.

## Publicación: ejecutar sólo con autorización específica

El mensaje inicial del relevo autoriza trabajo local. Si no hay permiso de commit/push/publicación, dejar Status: ready-for-human y entregar el resultado concreto. No solicitar autorización al principio de la implementación: preparar y verificar primero.

Cuando el humano autorice la publicación:

1. Releer infraestructura vigente de AGENTS.md y README; raíz Git, origin exacto, rama y diff de archivos propios.
2. Verificar que la rama/publicación acordadas son correctas. Usar codex/ para una rama nueva si hace falta; no mezclar ni resetear trabajo ajeno.
3. Preparar el commit sólo con archivos propios revisados. Evitar git add . por la existencia de cambios ajenos/no rastreados.
4. Antes de llevarlo a master, confirmar que esa acción está cubierta por la autorización: push a master dispara producción.
5. Utilizar el publicador único .github/workflows/deploy-closer-pages.yml. No habilitar el vínculo nativo antiguo ni reemplazarlo con una publicación manual habitual.
6. Esperar el workflow del SHA exacto. Un job aprobado/iniciado no equivale a workflow exitoso.
7. Confirmar Pages/account/project/production branch y canonical_deployment con SHA coincidente, mediante el verificador existente y acceso autorizado. Mantener credenciales en almacén privado/entorno; no copiarlas al chat o Git.
8. Exportar exactamente el contenido de ese SHA y verificar ambos dominios. build_site.py marca el working tree aunque se le pase un SHA: el argumento no prueba que sean iguales. Preferir un checkout/worktree administrado del SHA observado sin cambios públicos; o comparar cada archivo del paquete con su blob Git de ese SHA, incluidos HTML/assets nuevos. No exigir limpieza de cambios ajenos no exportados ni descartarlos. Si hay una diferencia pública, no usar ese export como prueba de la versión.

~~~powershell
$releaseSha = '<SHA_COMPLETO_DEL_WORKFLOW_OBSERVADO>'
# Desde el checkout verificado de ese SHA.
if ((git rev-parse HEAD).Trim() -ne $releaseSha) { throw 'El checkout no coincide con la version publicada.' }
python tools/build_site.py --commit $releaseSha
# Usar PUBLIC_SITE_DIR observado en el comando anterior.
python tools/check_hosting.py --commit $releaseSha --public-dir '<PUBLIC_SITE_DIR_OBSERVADO>'
~~~

El verificador necesita CLOUDFLARE_ACCOUNT_ID y CLOUDFLARE_API_TOKEN autorizados en el entorno. El workflow ya dispone de su credencial. Si localmente no está disponible, observar evidencia completa del verificador ejecutado por ese workflow; no obtener otro token ni inventar una pasada local.

9. El resultado exige workflow exitoso, deployment productivo del SHA y ambos hosts sirviendo todas las páginas/recursos del export. No basta un HTTP 200.
10. Navegador público: una guía/caso, recursos, contacto, móvil y carga automática de GA4 sin banner. Verificar eventos reales si la fase A de 04 está autorizada/configurada; esa recepción permite cerrar su fase B. Completar medición pública de rendimiento de las nuevas rutas sin atribuir datos de la versión anterior.
11. Registrar fecha D0, SHA, versión/URLs y evidencia. No declarar aceptación humana por haber publicado.

Si falla: identificar fase y preservar evidencia. No publicar por un proveedor alternativo, reintentar a ciegas ni ejecutar rollback de producción sin autorización para ese cambio. Preparar opción de recuperación usando el historial existente.

## Rastreo posterior

Releer sitemap desde ambos hosts y propiedad Search Console correcta. El sitemap puede actualizarse sin volver a dar de alta la propiedad. Observar cobertura/canonical seleccionado en las URLs prioritarias.

Solicitud de indexación, envío/cambio de sitemap en una consola y habilitación de IndexNow son acciones externas; realizar sólo si están incluidas en la autorización. La lectura de inspección no las autoriza. No pedir indexación repetidamente para ocultar un problema de calidad o canonical.

Registrar a D+7 y luego en los cortes de evaluación. No modificar noindex histórico para inflar cifras.
