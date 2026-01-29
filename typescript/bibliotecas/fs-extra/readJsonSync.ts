import pkg from "fs-extra"
const { readJsonSync } = pkg


const config = readJsonSync("output.json")
console.log("retorno da funcao:", config)
console.log("Valor do objeto dentro do json:", config.targetFolder)