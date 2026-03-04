import matter from "gray-matter";
import type { Document, Question, Book } from "../models/document";
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

  parseBook(content: string, filename: string): Book{
    const titleBookPattern =/^(.+?) - (?:(\d+)\s*ed\.?\s* - )?(.+?)\.md$/;
    const chapterPattern = /- \[\[Capítulo\s+\d+\s+-\s+.+?\]\]/g;

    const match = filename.match(titleBookPattern);

    if (!match) {
      throw new Error("Filename fora do padrão esperado.");
    }

    const title = match[1]!.trim();
    console.log("match:", match)
    const edition = match[2] ? parseInt(match[2], 10) : 1;

    let authors = [""]

    try {
      authors = match[3]!
        .split(",")
        .map(author => author.trim());
    } catch {
      console.log("parseBook: O autor nao foi especificado em", match[0])
    }

    const chaptersMatches = content.match(chapterPattern) || [];

    const chapters = chaptersMatches.map(chapter =>
      chapter.replace(/^- \[\[|\]\]$/g, "").trim()
    );

    return {
      title,
      edition,
      authors,
      chapters,
      hasDocument: content.length > 1 ? 1 : 0
    }
  }
  

  parseChapter(){
    throw new Error("Method not implemented.");
  }

  parseCommonAsked(){
    throw new Error("Method not implemented.");
  }
}
