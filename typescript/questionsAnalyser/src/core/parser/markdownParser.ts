import matter from "gray-matter";
import type { Document, Question } from "../models/document";
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

  parseQuestion(content: string, filename: string): Question {
    // Task to refactor
    // /^P(\d+)\.(\d+)\s*-\s*([^-]+)/
    // Aí você captura:
    // Grupo 1 → capítulo
    // Grupo 2 → número da questão
    // Grupo 3 → bookId

    const titleRegex = /^(P\d+\.\d+\s-\s[^-]+)/
    const titleContent = filename.match(titleRegex)

    const questionRegex = /\*\*Pergunta.*?\n([\s\S]*?)\*\*/;
    const questionContent = content.match(questionRegex)

    const answerRegex = /Resposta.*?\n```([\s\S]*?)```/
    const answerContent = content.match(answerRegex)

    const bookIdRegex = /^P\d+\.\d+\s*-\s*([^-]+?)\s*(?:-|$)/
    const bookIdContent = filename.match(bookIdRegex)

    const chapterRegex = /^P(\d+)\.\d+/
    const chapterContent = filename.match(chapterRegex)

    return {
      title: titleContent?.[1]?.trim() || "Not found",
      question: questionContent?.[1]?.trim() || "Not found",
      answer: answerContent?.[1]?.trim() || "Not found",
      bookId: bookIdContent?.[1]?.trim() || "Not found",
      chapter: chapterContent?.[1] ? parseInt(chapterContent[1], 10) : null,
      hasDocument: Number(content.length > 1)
    }
  }

  parseBook(){
    throw new Error("Method not implemented.");
  }

  parseChapter(){
    throw new Error("Method not implemented.");
  }

  parseCommonAsked(){
    throw new Error("Method not implemented.");
  }
}
