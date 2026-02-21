import type { FileProvider } from "./fileProvider";
type filesVerified = Record<string,string>

export class DocumentValidator {
  private bookPattern: RegExp;
  private titleBookPattern: RegExp;
  private chapterPattern: RegExp;
  private titleChapterPattern: RegExp;
  private commonAskedPattern: RegExp;
  private titleCommonAskedPattern: RegExp;
  private questionPattern: RegExp;
  private titleQuestionPattern: RegExp;
  private answeredPattern: RegExp;


  constructor(
    private readonly fileProvider: FileProvider,
  ) {
    this.bookPattern = /./;
    this.titleBookPattern = /^(.+?) - (?:(\d+ ed\.) - )?(.+)$/;
    this.chapterPattern = /./;
    this.titleChapterPattern = /^Cap[ií]tulo (\d+) - ([A-Za-z0-9&]+)(?: - (.+))?$/;
    this.commonAskedPattern = /./;
    this.titleCommonAskedPattern = /^Perguntas Comum(?: (\d+))? - ([A-Za-z0-9&]+) - Cap[ií]tulo (\d+)$/;
    this.questionPattern = /./;
    this.titleQuestionPattern = /^([A-Za-z])(\d+)\.(\d+) - ([A-Za-z0-9&]+) - (.+)$/;
    this.answeredPattern = /./;
  }

  async verifyTitles(): Promise<filesVerified> {
    const files = await this.fileProvider.listMarkdownFiles();
    const badFormat: Record<string, string> = {};

    for (const [index, path] of files.entries()){
      try {
        const filename = this.fileProvider.filenameOnly(path)
        let isBook = this.titleBookPattern.test(filename)
        let isChapter = this.titleChapterPattern.test(filename)
        let isCommonAsked = this.titleCommonAskedPattern.test(filename)
        let isQuestion = this.titleQuestionPattern.test(filename)
        if(isBook){
          continue;
        } else if (isChapter) {
          continue;
        } else if (isCommonAsked){
          continue;
        } else if (isQuestion){
          continue;
        } else {
          badFormat[filename] = 'no pattern'
        }

        if (index === files.length - 1) {
          console.log("Arquivos desformatados:", badFormat)
          return badFormat;
        }
      } catch (err) {
        console.warn(`Falha ao verificar padrão ${path}:`, err);
      }
    }
    
    console.log("não foi possível verificar seus arquivos.")
    return {}
  }

  async verifyFiles(): Promise<filesVerified> {
    const files = await this.fileProvider.listMarkdownFiles();
    const badFormat = {};

    for (const [index, path] of files.entries()){
      try {
        const content = await this.fileProvider.readFile(path);
        const filename = this.fileProvider.filenameOnly(path)
        let isBook = this.titleBookPattern.test(filename)
        let isChapter = this.titleBookPattern.test(filename)
        let isCommonAsked = this.titleBookPattern.test(filename)
        let isQuestion = this.titleBookPattern.test(filename)
        if(isBook){

        } else if (isChapter) {

        } else if (isCommonAsked){

        } else if (isQuestion){

        }
      } catch (err) {
        console.warn(`Falha ao verificar padrão ${path}:`, err);
      }
    }

    return badFormat
  }

  async verifyOneFile(path: string): Promise<string> {
    return "Não foi possível verificar o arquivo."
  }

  async onlyQuestionsTitle(): Promise<string[]>{
    const response = []
    const files = await this.fileProvider.listMarkdownFiles();
    for(const path of files){
      try {
        const filename = this.fileProvider.filenameOnly(path)
        let isQuestion = this.titleQuestionPattern.test(filename)
        if(isQuestion){
          response.push(path)
        }
      } catch(err){
        console.warn(`Falha ao retornar as questões ${path}`, err)
      }
    }

    
    return response
  }
}