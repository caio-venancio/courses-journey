import puppeteer from 'puppeteer';
// Or import puppeteer from 'puppeteer-core';

// Launch the browser and open a new blank page.
console.log("Comecando...")
const browser = await puppeteer.launch();
const page = await browser.newPage();

console.log("Indo para a página...")
// Navigate the page to a URL.
await page.goto('https://developer.chrome.com/');

console.log("Redimensionando...")
// Set screen size.
await page.setViewport({width: 1080, height: 1024});

console.log("Pressionando /...")
// Open the search menu using the keyboard.
await page.keyboard.press('/');

// Não funcionou esta parte
// console.log("Localizando accessibilidade...")
// Type into search box using accessible input name.
// await page.locator('::-p-aria(Search)').fill('automate beyond recorder');

// console.log("Localizando link...")
// Wait and click on first result.
// await page.locator('.devsite-result-item-link').click();

console.log("Selecionando texto...")
// Locate the full title with a unique string.
const textSelector = await page
  .locator('h2')
  .waitHandle();
const fullTitle = await textSelector?.evaluate(el => el.textContent);

// Print the full title.
console.log('The title of this blog post is "%s".', fullTitle);

await browser.close();