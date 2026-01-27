import type { FileProvider } from "../core/parser/fileProvider.js";
import { readFile } from "fs/promises";
import fg from "fast-glob";

export class NodeFileProvider implements FileProvider {
  async listMarkdownFiles(): Promise<string[]> {
    return fg("**/*.md", { ignore: ["node_modules"] });
  }

  async readFile(path: string): Promise<string> {
    return readFile(path, "utf-8");
  }
}
