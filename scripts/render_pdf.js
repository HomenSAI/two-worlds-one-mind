// Print a self-contained HTML file to PDF with headless Chromium (puppeteer).
// usage: node render_pdf.js input.html output.pdf "<footer html>"
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const [, , input, output, footer] = process.argv;
  const browser = await puppeteer.launch({
    executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/chromium',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
  });
  try {
    const page = await browser.newPage();
    // The book needs no network at all: fail loudly if anything tries to load an external resource.
    const external = [];
    await page.setRequestInterception(true);
    page.on('request', (req) => {
      const u = req.url();
      if (u.startsWith('file:') || u.startsWith('data:') || u.startsWith('about:')) return req.continue();
      external.push(u);
      return req.abort();
    });
    await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
    await page.emulateMediaType('print');
    await page.pdf({
      path: output,
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: footer,
      margin: { top: '18mm', bottom: '20mm', left: '16mm', right: '16mm' },
      preferCSSPageSize: false,
      outline: true,
      tagged: true,
    });
    if (external.length) {
      console.error('External resources were requested:\n' + external.join('\n'));
      process.exitCode = 2;
    }
  } finally {
    await browser.close();
  }
})();
