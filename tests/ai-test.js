// Test end-to-end: aplikacja + prawdziwy model AI w przeglądarce (uruchamiany w GitHub Actions).
const { chromium } = require('playwright');
(async () => {
  // zwykły (nie-incognito) profil przeglądarki – jak w telefonie, z normalnym limitem pamięci
  const b = await chromium.launchPersistentContext('/tmp/dziobsi-profile', { viewport: { width: 390, height: 844 } });
  const p = b.pages()[0] || await b.newPage();
  p.on('pageerror', e => console.log('PAGEERROR', e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto('http://localhost:8080/');
  await p.waitForFunction(() => window.Brain && Brain.ready && window.DziobLLM, null, { timeout: 60000 });
  await p.waitForTimeout(3000); // service worker + ewentualne przeładowanie
  await p.waitForFunction(() => window.Brain && Brain.ready && window.DziobLLM, null, { timeout: 60000 });
  console.log('crossOriginIsolated:', await p.evaluate(() => self.crossOriginIsolated), 'wątki CPU:', await p.evaluate(() => navigator.hardwareConcurrency));
  const t0 = Date.now();
  await p.evaluate(() => DziobLLM.load());
  let last = '';
  while (true) {
    const info = await p.evaluate(() => DziobLLM.info());
    const line = info.state + ' ' + Math.round(info.progress * 100) + '%';
    if (line !== last) { console.log('MODEL', line, Math.round((Date.now() - t0) / 1000) + 's'); last = line; }
    if (info.state === 'ready') { console.log('MODEL zapis w pamięci:', info.noCache ? 'NIE (brak miejsca)' : 'tak', '| GPU:', info.gpu, '| wątki:', info.threads); break; }
    if (info.state === 'error') { console.log('MODEL ERROR', info.error); process.exit(1); }
    await p.waitForTimeout(3000);
  }
  const ask = async q => {
    const s = Date.now();
    await p.fill('#input', q);
    await p.press('#input', 'Enter');
    await p.waitForFunction(() => !document.querySelector('.typing') && !document.querySelector('#btnSend').disabled, null, { timeout: 300000 });
    const ans = await p.evaluate(() => { const m = [...document.querySelectorAll('.msg.bot')].pop(); return m ? m.innerText.replace(/Jeśli masz jeszcze[^\n]*\n*/, '').replace(/\n+/g, ' | ') : ''; });
    const err = await p.evaluate(() => window.__aiError || '');
    const tm = await p.evaluate(() => DziobLLM.info().lastTimings);
    console.log(`>> ${q}   (${Math.round((Date.now() - s) / 1000)}s, prompt ${tm ? tm.cache_n + '+' + tm.prompt_n : '?'} tok)${err ? '  BŁĄD: ' + err : ''}\n   ${ans.slice(0, 300)}`);
  };
  // rozmowa ze zrzutów użytkownika
  const part1 = ['cześć!', 'Eli', 'Ale co', 'O czym', 'Zaproponuj cos', 'Powtarzasz po mnie', 'Może pogadamy o basenie?', 'Lubię pływać żabką'];
  const part2 = ['Elo mirdo', 'Nie wiem', 'Jakim modelem jestes', 'Ok', 'Mam pytanie czy ty znasz bartka', 'Ni to pytam', 'Ja mam na imie karol', 'I mam 27737373 lat', 'Ale co bylo?', 'No nie wiem o co ci chodzi', 'jak mam na imię?', 'co to jest fotosynteza?'];
  for (const q of part1) await ask(q);
  console.log('--- ponowne uruchomienie aplikacji (jak zamknięcie i otwarcie) ---');
  await p.reload();
  await p.waitForFunction(() => window.DziobLLM && DziobLLM.ready, null, { timeout: 300000 });
  for (const q of part2) await ask(q);
  await p.screenshot({ path: 'ai-test.png' });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
