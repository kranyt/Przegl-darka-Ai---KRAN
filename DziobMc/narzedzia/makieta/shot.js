const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
const tpl=fs.readFileSync('ui.html','utf8').replace('BG','file://'+process.argv[2]);
for(const [part,out] of [['hud.txt',process.argv[3]],['tab.txt',process.argv[4]]]){
 fs.writeFileSync('page.html',tpl.replace('BODY',fs.readFileSync(part,'utf8')));
 await p.goto('file://'+process.cwd()+'/page.html');await p.waitForTimeout(400);await p.screenshot({path:out});}
await b.close();})();
