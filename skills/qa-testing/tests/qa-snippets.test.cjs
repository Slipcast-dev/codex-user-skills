// Исполняются фрагменты самого навыка: фикстуры моделируют только используемые DOM-свойства.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const blocks = [...fs.readFileSync(process.argv[2] || require('node:path').join(__dirname, '../SKILL.md'), 'utf8').matchAll(/```javascript\n([\s\S]*?)```/g)].map(m=>m[1]);
const images = [
  {complete:false,naturalWidth:0,naturalHeight:0,src:'https://example.com/lazy.png',alt:''},
  {complete:true,naturalWidth:100,naturalHeight:80,src:'https://example.com/good.png',alt:'Фото'},
  {complete:true,naturalWidth:0,naturalHeight:0,src:'https://example.com/bad.png',alt:'Ошибка'},
].map(i=>({...i,hasAttribute:n=>n==='alt'}));
function context() {
  const logs=[];
  return {logs,console:{log:v=>logs.push(v),table:()=>{},warn:()=>{}},URL,
    window:{location:{href:'https://example.com/page',host:'example.com',hostname:'example.com'}},
    document:{title:'Коротко',documentElement:{lang:'ru'},querySelector:()=>undefined,
      getElementById:id=>['main','тест'].includes(id)?{id}:null,
      querySelectorAll:s=>s==='img'?images:s==='a[href^="#"]'?[
        {hash:'#main',textContent:'Перейти к содержимому'},
        {hash:'#%D1%82%D0%B5%D1%81%D1%82',textContent:'Перейти к тесту'},
        {hash:'#%ZZ',textContent:'Повреждённый якорь'},
      ]:[]}};
}
let checks=0;
function equal(actual,expected) {assert.deepEqual(actual,expected);checks++;}
for (const name of ['smoke','audit']) {
  const block=blocks.find(b=>b.includes(`const ${name} =`));
  const result=JSON.parse(vm.runInNewContext(block+`\nJSON.stringify(${name})`,context()));
  equal(result.brokenImages,1);
  equal(result.pendingImages,1);
  if(name==='audit') equal(result.skipLinkCandidates.map(x=>x.text),['Перейти к содержимому','Перейти к тесту']);
}
const c=context();
vm.runInNewContext(blocks.find(b=>b.includes('const imgs =')),c);
equal(c.logs[0].broken,1);equal(c.logs[0].pending,1);
const d=context();
d.document.querySelectorAll=()=>[
  {href:'https://example.com/local',target:'_blank',rel:''},
  {href:'https://example.com.evil.test/path',target:'_blank',rel:''},
  {href:'https://other.test/path',target:'_blank',rel:'noopener'},
];
const result=JSON.parse(vm.runInNewContext(blocks.find(b=>b.includes('const externalLinks ='))+'\nJSON.stringify({count:externalLinks.length,issues:issues.map(x=>x.href)})',d));
equal(result.count,2);equal(result.issues,['https://example.com.evil.test/path']);
console.log(JSON.stringify({checks,passed:true}));
