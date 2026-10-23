# 18 · Publicar la versión autorizada y comprobarla

Status: ready-for-human
Blocked by: 17; autorización específica de commit/push/publicación

## Entrega

Ambos dominios sirven la versión y recursos del SHA autorizado, mediante el publicador vigente.

## Pasos

1. Verificar autorización y destino exacto; seguir sección Publicación de validacion-publicacion.md.
2. Comprobar raíz, origin, rama, archivos propios y diff.
3. Preparar commit y llevarlo a master sólo si la autorización abarca esa operación.
4. Esperar workflow del SHA exacto; confirmar deployment productivo y canonical_deployment.
5. Verificar export con marcador, ambos dominios y recursos usando procedimiento existente.
6. Hacer comprobación pública funcional y registrar D0 por tanda/URL.

## Aceptación

- [ ] Autorización concreta y archivos propios revisados.
- [ ] Workflow exitoso del SHA; destino exacto.
- [ ] Verificador confirma ambos hosts y paquete correspondiente.
- [ ] Prueba pública observada, sin envío de consultas.
- [ ] D0/URLs/evidencia y medición activa o desactivada declarados.

Sin autorización, permanecer listo para humano. Un error de deploy no autoriza otro proveedor ni rollback automático.

## Registro de ejecución

Autorización / SHA / workflow / deployment / verificación / D0: pendiente.
