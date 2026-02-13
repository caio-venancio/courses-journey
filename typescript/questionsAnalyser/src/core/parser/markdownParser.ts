import matter from "gray-matter";
import type { Document } from "../models/document";
import { randomUUID } from "crypto";

export class MarkdownParser {


  parse(content: string, path: string): Document {
    const { data, content: body } = matter(content);

    return {
      id: randomUUID(),
      path,
      title: data.title ?? path.split("/").pop() ?? "Sem título",
      content: body,
      livro: data.livro,
      capitulo: data.capitulo,
      tipo: data.tipo,
      tags: data.tags ?? []
    };
  }

  parseQuestion(){}
}
