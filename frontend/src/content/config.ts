import { defineCollection, z } from 'astro:content';

const tilCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    publishDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    snippet: z.string().optional(),
  }),
});

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    topic: z.enum(['tecnología', 'tecno-política', 'gaming', 'hardware', 'general']).default('general'),
    draft: z.boolean().default(false),
  }),
});

const labCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    status: z.enum(['active', 'prototype', 'wip', 'archived']).default('wip'),
    stack: z.array(z.string()).default([]),
    repoUrl: z.string().url().optional(),
    demoUrl: z.string().url().optional(),
    updatedDate: z.coerce.date(),
  }),
});

const hobbiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    category: z.enum(['pokemon', 'gaming', 'hardware', 'coleccionismo', 'curiosidades']),
    date: z.coerce.date(),
    status: z.string().optional(),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = {
  til: tilCollection,
  blog: blogCollection,
  lab: labCollection,
  hobbies: hobbiesCollection,
};

