const { createInterface } = require('node:readline');

const rl = createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: 'heheh> ',
});


rl.prompt();

rl.on('line', (line) => {
switch (line.trim()) {
    case 'hello world':
      console.log('Terminando!');
      rl.close();
      process.exit(0);
    default:
      console.log(`Say what? I might have heard '${line.trim()}'`);
      break;
  }

rl.prompt();
})