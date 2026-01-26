const puppeteer = require('puppeteer');
const fs = require('fs');

async function salvarHTMLDoSite(url, nomeArquivo) {
    // 1. Inicia o navegador
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    try {
        // 2. Navega até a URL
        await page.goto(url, { waitUntil: 'networkidle2' }); // Aguarda a página carregar
        
        // 3. Pega o conteúdo HTML
        const html = await page.content();

        // 4. Salva o HTML em um arquivo local
        fs.writeFile(nomeArquivo, html, (err) => {
            if (err) throw err;
            console.log(`Arquivo ${nomeArquivo} salvo com sucesso!`);
        });
    } catch (error) {
        console.error('Erro ao acessar o site:', error);
    } finally {
        // 5. Fecha o navegador
        await browser.close();
    }
}

// Uso da função
salvarHTMLDoSite('https://www.example.com', 'site.html');