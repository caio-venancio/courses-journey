import fg from 'fast-glob'

const entries = await fg(['.editorconfig', '**/index.js'], { dot: true })

console.log("Encontrei estes:", entries)