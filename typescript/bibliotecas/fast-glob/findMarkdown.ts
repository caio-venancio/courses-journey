import fg from 'fast-glob'

const entries = await fg(['**/*.md'], { dot: true })

console.log("Encontrei estes:", entries)