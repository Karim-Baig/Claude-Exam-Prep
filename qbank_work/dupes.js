// Pairwise near-duplicate scan over the merged bank.
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'claude-foundations-exam.html'), 'utf8');
const QB = [];
eval([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1])
      .filter(s => s.includes('QB.push')).join('\n'));
const norm = s => new Set(String(s).toLowerCase().replace(/[^a-z0-9 ]/g, ' ')
                    .split(/\s+/).filter(w => w.length > 4));
const sig = QB.map(q => ({ q, set: norm(q.q + ' ' + q.o.join(' ')) }));
const hits = [];
for (let i = 0; i < sig.length; i++) {
  for (let j = i + 1; j < sig.length; j++) {
    if (sig[i].set.size < 8 || sig[j].set.size < 8) continue;
    const inter = [...sig[i].set].filter(x => sig[j].set.has(x)).length;
    const jac = inter / (sig[i].set.size + sig[j].set.size - inter);
    if (jac > 0.5) hits.push([jac, sig[i].q, sig[j].q]);
  }
}
hits.sort((a, b) => b[0] - a[0]);
console.log('Pairs above 0.50 Jaccard:', hits.length, ' of', QB.length * (QB.length - 1) / 2, 'pairs\n');
hits.forEach(([jac, a, b]) => {
  console.log(`${jac.toFixed(2)}  #${a.id} [${a.d}/${a.s}]  <->  #${b.id} [${b.d}/${b.s}]`);
  console.log('    A: ' + a.q.replace(/\n/g, ' ').slice(0, 120));
  console.log('    B: ' + b.q.replace(/\n/g, ' ').slice(0, 120));
});
