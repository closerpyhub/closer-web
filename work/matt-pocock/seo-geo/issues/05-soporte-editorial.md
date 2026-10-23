# 05 · Habilitar páginas editoriales sin perder controles

Status: done
Blocked by: None

## Entrega

Una guía/caso completo puede validarse y exportarse como artículo, conservando páginas y servicios actuales.

## Pasos

1. Seguir cambios exactos del checker en arquitectura.md.
2. Separar conjunto de servicios del crecimiento de rutas requeridas; añadir clasificación editorial progresiva.
3. Validar WebPage + Article y OG correspondiente; mantener referencias de grafo autocontenidas.
4. Añadir pruebas focalizadas de clasificación, grafo, OG, sitemap y enlaces con Python unittest.
5. Añadir prueba de export que incluye una página/imagen pública y excluye documentación/evidencia.
6. Conservar build filtrado, hashes y comportamiento de hosting. Usar fixtures temporales, no un artículo placeholder público.

## Aceptación

- [ ] Servicios originales conservan Service y las exclusiones noindex.
- [ ] Artículo válido pasa y artículo mal clasificado falla.
- [ ] Nuevos controles no se eluden debilitando los existentes.
- [ ] Export no incorpora documentación, borradores ni datos privados.
- [ ] Pruebas actuales y nuevas pasan.

## Registro de ejecución

Cambios: `tools/check_site.py` separa servicios de artículos, exige `Article`/`WebPage` autocontenidos y `og:type=article` en las seis guías. Pruebas: se añadieron `tools/test_check_site.py` y `tools/test_build_site.py`; la prueba de clasificación falló antes de implementar la regla y luego pasó. Resultado: `python tools/check_site.py` pasó con 32 páginas/28 URLs; `python -m unittest discover -s tools -p 'test_*.py'` pasó con 12 pruebas. El export de prueba incluyó 54 archivos públicos y excluyó `work/`, `materials/` y `tools/`.
