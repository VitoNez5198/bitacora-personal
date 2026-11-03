# Diseño Técnico: Adaptabilidad Móvil Sobria

## Arquitectura y Estrategia de Diseño

Para preservar la identidad de ingeniería minimalista y 0 KB de JavaScript innecesario, la solución se basa 100% en utilidades responsivas de Tailwind CSS y CSS nativo en Astro, sin añadir scripts de hidratación del lado del cliente.

---

## 1. Modificaciones en el Layout Base (`src/layouts/BaseLayout.astro`)

### Cabecera (Header)
```astro
<!-- Estructura responsiva de la barra de navegación -->
<header class="border-b border-carbon-700/70 bg-carbon-900/95 backdrop-blur sticky top-0 z-50">
  <div class="max-w-4xl mx-auto px-3 sm:px-6 min-h-12 sm:h-14 py-2 sm:py-0 flex flex-wrap sm:flex-nowrap items-center justify-between gap-2">
    <!-- Prompt shell con truncado seguro en móviles -->
    <a href="/" class="flex items-center gap-1.5 sm:gap-2 text-xs font-mono text-syntax-muted hover:text-syntax-text">
      <span class="inline-block w-2 h-2 rounded-full bg-syntax-accent animate-pulse"></span>
      <span class="hidden xs:inline text-syntax-subtle">user@garden:</span>
      <span class="text-syntax-accent">~{currentPath !== "/" ? currentPath : ""}</span>
    </a>

    <!-- Navegación táctil compacta -->
    <nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-0.5">
      {navItems.map((item) => (
        <a
          href={item.href}
          class="px-2 py-1 text-[11px] sm:text-xs font-mono rounded whitespace-nowrap ..."
        >
          {item.label}
        </a>
      ))}
    </nav>
  </div>
</header>
```

### Contenedor Principal (Main)
- Cambiar padding horizontal de `px-4 sm:px-6` a `px-3 sm:px-6` en móviles para ganar 16px de ancho útil en lectura.
- Padding vertical ajustado: `py-6 sm:py-12`.

---

## 2. Hoja de Estilos Global (`src/styles/global.css`)

- **Scroll suave en bloques de código:**
  ```css
  .prose-garden pre {
    -webkit-overflow-scrolling: touch;
    overscroll-behavior-x: contain;
    border-radius: 4px;
    padding: 0.75rem 1rem;
  }
  ```
- **Tamaños tipográficos fluidos:** Reducir encabezados en pantallas móviles para evitar cortes de palabras en títulos técnicos.

---

## 3. Páginas de Sección (`index.astro`, `blog/`, `lab/`, `hobbies/`)

- Padding de tarjetas reducido de `p-5` a `p-4 sm:p-5`.
- Fechas y tags en disposición fluida (`flex-wrap`) para que nunca colisionen en pantallas estrechas.

