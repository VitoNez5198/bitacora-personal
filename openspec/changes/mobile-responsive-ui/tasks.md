# Tareas de Implementación: Optimización Móvil

- [ ] 1. **Optimizar `BaseLayout.astro` para pantallas pequeñas**
  - [ ] 1.1 Ajustar padding horizontal del header (`px-3 sm:px-6`) y altura flexible.
  - [ ] 1.2 Permitir scroll horizontal sutil o wrap en la barra de navegación para anchos < 380px.
  - [ ] 1.3 Ampliar área útil del contenedor `<main>` en pantallas móviles.

- [ ] 2. **Ajustar estilos globales en `global.css`**
  - [ ] 2.1 Agregar soporte de touch scroll y contención en `.prose-garden pre`.
  - [ ] 2.2 Escalar jerarquía de encabezados (`h1`, `h2`) en `.prose-garden` para pantallas pequeñas.

- [ ] 3. **Refinar vistas de contenido y lectura**
  - [ ] 3.1 Ajustar tarjetas en `src/pages/index.astro` a `p-4 sm:p-5`.
  - [ ] 3.2 Calibrar encabezado de artículos en `src/pages/blog/[...slug].astro` (`text-2xl sm:text-4xl`).
  - [ ] 3.3 Revisar disposición de tags y metadatos en `/lab` y `/hobbies` con `flex-wrap`.

- [ ] 4. **Verificación y Testing**
  - [ ] 4.1 Ejecutar `npm run build` para asegurar 0 errores de compilación.
  - [ ] 4.2 Probar visualmente en el navegador simulando dispositivos móviles (iPhone SE 375px y Pixel 412px).

