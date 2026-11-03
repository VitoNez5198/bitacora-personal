# Spec: Comportamiento y Responsive Móvil

## Requisitos del Sistema

### 1. Barra de Navegación Móvil
- **REQ-NAV-01:** La barra superior debe mantener una altura contenida en móviles (h-auto con padding vertical o h-14 flexible).
- **REQ-NAV-02:** En pantallas con ancho menor a 640px (`< sm`), los ítems de navegación (`~/stream`, `~/blog`, `~/lab`, `~/hobbies`) deben disponer de espaciado táctil adecuado y organizarse de modo que no se superpongan con el prompt `user@garden:~`.
- **REQ-NAV-03:** El identificador del prompt en pantallas muy pequeñas (< 380px) puede abreviarse a `~` o mantener un tamaño compacto `text-xs` para ceder espacio a los enlaces de sección.

### 2. Renderizado de Contenido y Artículos
- **REQ-PROSE-01:** Los títulos `h1` en móviles deben usar una escala adecuada (`text-2xl` a `text-3xl`) para evitar saltos de línea excesivos en títulos largos.
- **REQ-PROSE-02:** Los bloques de código `<pre>` deben incluir `-webkit-overflow-scrolling: touch`, `overflow-x: auto`, y un padding interno calibrado para pantallas táctiles.
- **REQ-PROSE-03:** Las imágenes y tablas deben tener `max-w-full` y scroll horizontal dedicado si exceden el viewport.

### 3. Tarjetas y Listados
- **REQ-CARD-01:** Las tarjetas del stream TIL (`/`), blog (`/blog`), laboratorio (`/lab`) y hobbies (`/hobbies`) deben utilizar padding adaptativo (`p-4` en móviles, `sm:p-5` en desktop).
- **REQ-CARD-02:** Los metadatos (fecha, tags y estado) deben distribuirse en columna o flex wrap limpio en móviles, sin romper el contenedor.

