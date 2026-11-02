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
  const questions = ['lubisz mnie?', 'kochasz mnie?', 'czy lubisz koty?', 'cześć, jak się masz?', 'byłem dziś na rowerze', 'co to jest fotosynteza?', 'opowiedz mi coś o Krakowie', 'sprawdź słowo dziób', 'zrób grę'];
  for (const q of questions) {
    const s = Date.now();
    await p.fill('#input', q);
    await p.press('#input', 'Enter');
    await p.waitForFunction(() => !document.querySelector('.typing') && !document.querySelector('#btnSend').disabled, null, { timeout: 300000 });
    const ans = await p.evaluate(() => { const m = [...document.querySelectorAll('.msg.bot')].pop(); return m ? m.innerText : ''; });
    const tm = await p.evaluate(() => DziobLLM.info().lastTimings);
    console.log(`\n>> ${q}   (${Math.round((Date.now() - s) / 1000)}s)${tm ? ' timings: ' + JSON.stringify(tm) : ''}\n${ans.slice(0, 400)}`);
  }
  await p.screenshot({ path: 'ai-test.png' });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
