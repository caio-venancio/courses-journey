import pkg from "fs-extra"
const { writeJsonSync } = pkg

const objeto = {
    targetFolder: "folder/do/bem"
}

writeJsonSync("output.json", objeto)


// 96 x 12
// file:///C:/Users/caiov/Tecnologia%20da%20Informacao/Projetos/courses-journey/typescript/bibliotecas/fs-extra/writeJsonSync.ts:1
// import { writeJsonSync } from "fs-extra"
// ^^^^^^^^^^^^^
// JS module, which may not support all module.exports as named exports.
// CommonJS modules can always be imported via the default export, for example using:

// import pkg from 'fs-extra';
// const { writeJsonSync } = pkg;

// The error message tells us exactly how to fix it. fs-extra is a CommonJS module, so we need to import it as a default export:

// Edited
// writeJsonSync.ts+2-1
// Fixed! The issue was using a named import from a CommonJS module in an ESM context. I've changed it to use a default import and then destructure the named export, which should resolve the error.