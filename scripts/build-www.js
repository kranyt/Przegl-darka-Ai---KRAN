// Kopiuje pliki aplikacji webowej do www/ (dla Capacitor / APK)
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const out = path.join(root, 'www');
const items = ['index.html', 'style.css', 'bigdict.js', 'brain.js', 'memory.js', 'talk.js', 'code.js', 'app.js', 'llm.js', 'vendor', 'sw.js', 'manifest.webmanifest', 'data', 'icons'];
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out);
for (const it of items) fs.cpSync(path.join(root, it), path.join(out, it), { recursive: true });
console.log('www/ gotowe');
