# 04 · Configurar y comprobar recepción real de medición

Status: done
Blocked by: ninguno

## Entrega

Propiedad y flujo correctos recibiendo eventos seguros de la versión publicada autorizada.

## Fase A · Preparación autorizada, antes de 17 si llegan las entradas

1. Recuperar datos/permiso existentes o pedir la entrada exacta; no crear otra propiedad por suposición.
2. Preparar la configuración externa concreta definida en medicion.md y obtener autorización si falta.
3. Desactivar captura automática riesgosa, publicidad/señales y dejar retención documentada; releer lo persistido.
4. Incorporar ID real al HTML local; probar con intercepción. Registrar este subpaso listo antes del ticket 17 si las entradas llegan a tiempo.

## Fase B · Recepción, después de 18

5. Observar recepción en la propiedad correcta mediante debug/pruebas identificadas.
6. Documentar límites por consentimiento, filtros y datos de prueba. Sólo entonces cerrar 04.

## Aceptación

- [x] Propiedad/flujo y autorización comprobados.
- [x] Configuración persistida coherente con el contrato.
- [x] Recepción real observada y separada de pruebas locales.
- [x] No hay eventos duplicados ni contenido personal en payload.

Este ticket no bloquea 17/18. Si no se completa, publicar la implementación desactivada y declararlo. Si se recibe ID después de publicar, preparar y validar un cambio posterior cuya publicación también requiere autorización.

## Registro de ejecución

23/10/2026 · Se verificó sólo por nombres de archivo y variables de entorno (sin leer secretos) que el repositorio versionado y este entorno no contienen un ID GA4/GTM o una configuración de medición reutilizable. No se creó otra propiedad, no se añadió un tracker, no se activó captura automática ni se modificó Cloudflare Web Analytics. Faltan el ID público de una propiedad existente, los hechos E03/E04 del aviso de privacidad y la autorización para configurar/validar la recepción.

23/10/2026 · La persona responsable autorizó la creación de una propiedad GA4 para Closer y se configuró la fuente web `https://closer.com.py` con medición mejorada desactivada. También se desactivaron Signals y personalización publicitaria; no se añadieron píxeles ni GTM. El código local usa el ID público de esa fuente, pero la prueba local bloqueó la carga de la etiqueta y no contaminó la propiedad. Después de publicar, falta observar un evento de prueba sin datos personales en la propiedad correcta antes de cerrar este ticket.

23/10/2026 · Tras el despliegue del SHA `b155be1449cdd018e384afaf2042091cf45303cb`, se autorizó y realizó una única visita de prueba consentida en `https://closer.com.py`. Google Analytics de la propiedad `Closer | sitio web` mostró 1 usuario activo durante los últimos 30 minutos, país Paraguay. La visita no completó formularios ni enlaces de contacto; sólo confirmó la llegada de la medición consentida. Esto cierra la recepción real sin confundir un clic con una consulta comercial.
