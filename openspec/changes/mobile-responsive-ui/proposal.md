# Propuesta: Optimización Móvil y Responsive del Jardín Digital

## Contexto y Motivación
La bitácora personal fue diseñada con una estética de terminal sobria y minimalista. Si bien el layout actual utiliza clases responsivas básicas de Tailwind CSS, la experiencia de lectura en dispositivos móviles (smartphones con anchos de 360px a 430px) presenta detalles que pueden optimizarse para una navegación táctil impecable:

1. **Barra de navegación superior:** En pantallas estrechas, los 4 enlaces (`~/stream`, `~/blog`, `~/lab`, `~/hobbies`) junto al prompt del usuario (`user@garden:~`) pueden amontonarse o desbordar la altura de la cabecera.
2. **Bloques de código y preformateados:** En móviles, los fragmentos de código largos necesitan un scroll horizontal fluido con indicador visual para evitar romper el ancho de la pantalla (*horizontal scroll blowout*).
3. **Áreas táctiles (Tap Targets):** Los botones y enlaces pequeños deben cumplir con una zona de pulsación mínima cómoda (40px–44px) sin perder su elegancia compacta.
4. **Tipografía y lectura en pantalla chica:** Ajustar el espaciado y márgenes de los artículos (`.prose-garden`) para aprovechar el ancho útil del celular sin cansar la vista.

---

## Objetivos (Goals)
- Garantizar que la barra superior se adapte fluidamente en pantallas menores a 640px sin saltos de línea bruscos ni desbordes.
- Optimizar el contenedor `.prose-garden` para lectura móvil: títulos proporcionados, bloques de código con scroll táctil suave y párrafos sin márgenes laterales excesivos.
- Mejorar los tags y enlaces de navegación con áreas táctiles accesibles.
- Mantener estrictamente la filosofía **cero clichés de IA**: nada de hamburguesas con animaciones pesadas ni popups flotantes; la navegación móvil seguirá siendo limpia, sobria y rápida.

---

## No-Objetivos (Non-Goals)
- No se añadirá un menú flotante ni drawers deslizables pesados en JavaScript.
- No se agregará tracking ni librerías de analítica.
- No se modificará el esquema de base de datos ni el backend de FastAPI.

---

## Criterios de Aceptación
- La barra de navegación se visualiza sin desbordes horizontales en resoluciones desde 360px de ancho.
- Los bloques `<pre><code>` permiten desplazamiento horizontal táctil suave sin alterar el ancho del documento.
- Todas las secciones (`/`, `/blog`, `/blog/[slug]`, `/lab`, `/hobbies`) son 100% legibles y navegables con una sola mano en móviles.

