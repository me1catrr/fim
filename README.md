# FIM · Fundamentos de Ingeniería Mecánica

**Bloque 3: Mecánica del Medio Continuo y Teoría de Estructuras**

Máster Universitario en Ingeniería Industrial · Universidad de Córdoba
Profesor: Rafael Castro Triguero.

Repositorio público: <https://github.com/me1catrr/fim>.
**GitHub Pages no está activado.** Esta es únicamente la inicialización técnica:
no contiene todavía capítulos, laboratorios ni ejercicios desarrollados.
No sustituye a la guía docente oficial.

## Objetivos y organización académica

Preparar al alumnado para Elementos Finitos en segundo de Máster, conectando
principios físicos, cálculo manual, programación e interpretación estructural.

| Identificador | Ámbito | Encaje provisional |
|:--|:--|:--|
| F00 | Preparación matemática y computacional | Transversal |
| F01 | Tensiones, deformaciones y elasticidad lineal | Sesión 1 |
| F02 | Resistencia de Materiales, trabajo y energía | Sesión 2 |
| F03 | Método de la flexibilidad | Sesión 3 |
| F04 | Método matricial de rigidez | Sesión 4 |
| F05 | Proyecto integrador y transición conceptual al MEF | Sesión 5 |

Cinco sesiones de cuatro horas **incluyendo descansos**: 20 horas presenciales.
F00 no añade una sexta sesión. Cada sesión futura tendrá objetivos, tiempos,
ejercicios autocorregibles y laboratorio computacional. Esta distribución
es provisional y no desarrolla todavía el temario.

## Estructura

```text
fim/
├── .github/workflows/publish.yml
├── .gitignore
├── CLAUDE.md
├── README.md
├── _quarto.yml
├── index.qmd
├── chapters/
│   ├── f00-preparacion/
│   ├── f01-elasticidad/
│   ├── f02-resistencia-energia/
│   ├── f03-flexibilidad/
│   ├── f04-rigidez/
│   └── f05-proyecto/
├── practicas/
├── ejercicios/
│   ├── autocorreccion/
│   └── problemas/
├── interactive/
├── assets/
│   ├── css/fim.css
│   ├── js/
│   └── figures/
├── code/
│   ├── julia/
│   └── python/
├── references/
├── scripts/check_site.py
└── tests/test_check_site.py
```

Las carpetas reservadas se conservan con `.gitkeep`. `index.qmd` es la única
página del libro; los futuros capítulos se añadirán a `book.chapters`.
La salida HTML se genera en `_book/` y no se versiona.

## Requisitos

Para construir: Quarto 1.10.x. Para controles: Python 3.10 o posterior,
solo biblioteca estándar. Julia y Node.js quedan disponibles para el futuro
código científico y la interactividad; no son necesarios para renderizar
esta portada. No se requiere instalar paquetes de Python, Julia ni npm.

Versiones detectadas al inicializar:

| Herramienta | Versión |
|:--|:--|
| Git | 2.55.0 |
| GitHub CLI | 2.103.0 |
| Quarto | 1.10.19 |
| Julia | 1.12.3 |
| Python | 3.11.4 |
| Node.js | 26.12.0 |

## Desarrollo local

```sh
git clone https://github.com/me1catrr/fim.git ~/Proyectos/fim
cd ~/Proyectos/fim
quarto preview
```

Si ya existe la carpeta, inspeccionarla antes de clonar; no sobrescribirla.
Para validar desde la raíz:

```sh
python3 -m unittest discover -s tests -v
quarto render
python3 scripts/check_site.py
```

Abrir `_book/index.html` o utilizar `quarto preview`. El comprobador revisa
idioma, título, viewport, presencia de contenido principal, textos alternativos
de imágenes, recursos locales y enlaces internos con fragmentos.
No accede a webs externas ni ejecuta JavaScript; no sustituye la revisión
visual, de teclado y de consola del navegador.
No hay aún modelos numéricos que verificar ni JavaScript propio.

`execute.enabled: false` impide la ejecución de código durante el render
inicial. No hacen falta Jupyter, R ni paquetes de cálculo para esta portada.
Los futuros ejemplos definirán sus entornos y pruebas cuando se implementen.

## Reutilización y trabajo con asistentes

Consultar [CLAUDE.md](CLAUDE.md) antes de modificar el proyecto desde Cursor,
Claude Code u otro asistente. Los repositorios preferentes para analizar
material reutilizable son [resistencia](https://github.com/me1catrr/resistencia)
y [resonancia](https://github.com/me1catrr/resonancia), localizados inicialmente
en `../resistencia` y `../resonancia`.
No se ha copiado material de ellos y FIM no depende de esos clones.

## Publicación futura: desactivada

`.github/workflows/publish.yml` contiene el workflow de publicación, **bloqueado
por condición**. Solo admite ejecución manual (`workflow_dispatch`), desde
`main` y con la variable de repositorio `ENABLE_PAGES` igual a `true`.
Si la variable no existe o tiene otro valor, ambos trabajos se omiten.
No hay disparador por push ni por pull request. No se ha habilitado la variable.
Con autorización expresa, habrá que:

1. Revisar materiales, permisos y licencias antes de publicar el HTML.
2. Revisar el workflow y configurar Pages con origen GitHub Actions.
3. Crear la variable de repositorio `ENABLE_PAGES` con valor `true` en
   Settings → Secrets and variables → Actions → Variables.
4. Lanzar manualmente el workflow desde `main` y revisar el sitio resultante.

Para volver a bloquear futuras publicaciones, eliminar la variable o cambiarla
a `false`; esto no retira un sitio que ya se haya publicado.

No se han configurado Pages, dominio ni URL de sitio publicada.

## Licencias

Pendientes de decisión del propietario, tanto para código como para contenidos.
No se ha añadido ninguna licencia. La visibilidad pública no concede por sí
sola una licencia de reutilización.
