# 18 · Publicar la versión autorizada y comprobarla

Status: done
Blocked by: ninguno

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

23/10/2026 · La instrucción explícita “Haz TODO el plan por favor” autorizó ejecutar la publicación preparada. Se comprobó raíz `C:/Users/thoma/Documents/ChatGPT/Web Closer`, remoto `https://github.com/closerpyhub/closer-web.git`, rama `master` y cambios propios; `AGENTS.md` permaneció sin versionar. Se creó y publicó `f1ea30ce2705cd0a8d58ba0e122d5c67bd352a1f` (`feat: add SEO and GEO content hub`).

El workflow `Publish WEB Closer to its Cloudflare Pages project` terminó exitosamente en [run 39985742430](https://github.com/closerpyhub/closer-web/actions/runs/39985742430). Cloudflare de solo lectura confirmó la cuenta, zona `closer.com.py`, Pages `closer-web` (`089d08e6-cefa-4d17-91f0-a15571346a43`), rama `master`, despliegue productivo canónico `18772867-c3cf-4b17-9159-0d47b869ff4d`, SHA exacto y alias activos `closer.com.py` / `www.closer.com.py`.

Para evitar que la conversión de saltos de línea de Windows altere la comparación, se regeneró el export desde el blob Git del SHA publicado. La verificación pública completa aprobó los 54 artefactos y las 32 páginas con la marca `closer-release` en ambos dominios. D0 técnico: 23/10/2026; la medición comercial continúa desactivada por falta de ID/provisión y hechos de privacidad autorizados.

23/10/2026 · La ampliación autorizada de medición se publicó en `4fbd60a86b9c5e410e70eb9b20e5970ec3e95562`, y la corrección posterior de versión de caché en `b155be1449cdd018e384afaf2042091cf45303cb`. El workflow oficial terminó correctamente; Cloudflare confirmó ese SHA como despliegue productivo canónico, con ambos aliases activos. El export público actual aprobó 55 artefactos y 33 páginas en los dos dominios. La medición adicional quedó activa únicamente después de consentimiento y su recepción real consta en 04.
