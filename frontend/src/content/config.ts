import { defineCollection, z } from 'astro:content';

const notasCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    publishDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    snippet: z.string().optional(),
  }),
});

const historiasCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    topic: z.enum([
      'historia',
      'ciencia',
      'naturaleza',
      'sociedad',
      'tecnología',
      'cultura',
      'general'
    ]).default('general'),
    draft: z.boolean().default(false),
  }),
});

const curiosidadesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    publishDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    snippet: z.string().optional(),
  }),
});

const rinconCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    type: z.enum(['proyecto', 'tcg', 'gaming', 'coleccion', 'setup', 'general']).default('general'),
    date: z.coerce.date(),
    status: z.string().optional(),
    tags: z.array(z.string()).default([]),
    link: z.string().url().optional(),
  }),
});

export const collections = {
  notas: notasCollection,
  historias: historiasCollection,
  curiosidades: curiosidadesCollection,
  rincon: rinconCollection,
};
