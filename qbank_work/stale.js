// Inspect flagged stale-fact hits to separate genuine errors from legitimate
// use of a stale term as a distractor or as an explicitly-corrected point.
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'Claude Certified Developer - Foundations.html'), 'utf8');
const QB = [];
eval([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1])
      .filter(s => s.includes('QB.push')).join('\n'));
const LTR = ['A','B','C','D'];
const ids = [39, 1038, 1185, 1186, 1373, 1416, 1417, 1538, 1590, 1675, 2166];
ids.forEach(id => {
  const q = QB.find(x => x.id === id);
  if (!q) return;
  const term = /x-request-id/i.test(q.q + q.o.join(' ') + q.e + q.w) ? 'x-request-id'
             : /750/.test(q.q + q.o.join(' ') + q.e + q.w) ? '/750'
             : '-latest';
  console.log('==== #' + id + '  [' + q.d + '] term: ' + term);
  console.log('Q  : ' + q.q.replace(/\n/g, ' ').slice(0, 150));
  // where does the term appear?
  const re = term === '/750' ? /750/ : new RegExp(term.replace('-', '\\-'), 'i');
  q.o.forEach((o, k) => { if (re.test(o)) console.log('  ' + (k === q.a ? 'CORRECT>' : 'distract>') + ' ' + LTR[k] + '. ' + o.replace(/^[A-D]\. /, '').slice(0, 110)); });
  if (re.test(q.e)) {
    const s = q.e.split(/(?<=\.)\s+/).filter(x => re.test(x));
    console.log('  in e   : ' + s.join(' ').slice(0, 260));
  }
  if (q.w && re.test(q.w)) {
    const s = q.w.split(/(?<=\.)\s+/).filter(x => re.test(x));
    console.log('  in w   : ' + s.join(' ').slice(0, 260));
  }
  console.log('');
});
