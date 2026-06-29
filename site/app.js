
// Safe in this static demo: data.json is generated from repo-local synthetic artifacts,
// not from user-submitted browser input. innerHTML is used only to render fixed proof data.
function money(n){return '$'+Number(n||0).toLocaleString(undefined,{maximumFractionDigits:0})}
function cents(c){var n=Number(c||0);var sign=n<0?'-':'';return sign+'$'+(Math.abs(n)/100).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2})}
function clsForDecision(d){d=(d||'').toLowerCase();if(d.includes('block'))return 'block';if(d.includes('escalate'))return 'warn';return 'ok'}
function el(id){return document.getElementById(id)}
function tagList(items){return '<div class="tags">'+items.map(x=>'<span>'+x+'</span>').join('')+'</div>'}
function boot(){fetch('data.json?ts='+Date.now()).then(r=>r.json()).then(data=>{
  const a=data.audit||{}, e=data.evidence||{}, n=data.nvidia||{}, proof=data.proof||{}, safety=data.safety_log||{}, treasury=data.treasury||{}, f=data.format||{};
  el('spend').textContent=f.spend; el('savings').textContent=f.savings; el('fee').textContent=f.fee; el('runCost').textContent=f.run_cost;
  const nem=(n.nemotron_3_ultra||{}), claw=(n.nemoclaw||{}), skills=(n.nvidia_skills||{});
  el('nemotronCard').innerHTML=(nem.model||'Nemotron 3 Ultra')+' returned <b class="'+clsForDecision(nem.verdict)+'">'+(nem.verdict||'n/a')+'</b>'+(nem.latency_seconds?' in '+nem.latency_seconds+'s':'')+'.';
  el('clawCard').textContent=(claw.status||'scaffold only')+'. '+(claw.runtime_installed?'Runtime installed.':'Runtime not installed/claimed.');
  el('stripeCard').textContent=(treasury.mode||((data.ledger||{}).payment||{}).mode||'test/local')+'; ending balance '+f.balance+'.';
  el('generated').textContent='Generated '+(proof.generated_at||a.generated_at||'');
  const events=(safety.events||[]).slice(0,8);
  el('safetyEvents').innerHTML=events.map((x,i)=>'<div class="event"><b>#'+(i+1)+'</b><span>'+(x.step||x.action||x.kind)+'<br><small>'+(x.reason||x.model||x.kind||'policy checks recorded')+'</small></span><b class="'+clsForDecision(x.decision||x.nemotron_verdict)+'">'+(x.decision||x.nemotron_verdict||'checked')+'</b></div>').join('');
  const entries=(treasury.entries||((data.ledger||{}).entries)||[]);
  el('treasuryEntries').innerHTML=entries.map(x=>'<div class="line"><span>'+x.label+'<small>'+(x.timestamp||x.approved_by||'')+'</small></span><b class="'+(Number(x.amount_cents)>=0?'ok':'neg')+'">'+cents(x.amount_cents)+'</b></div>').join('')+'<div class="line"><span><b>Ending treasury</b></span><b class="ok">'+f.balance+'</b></div>';
  el('evidenceCards').innerHTML=(e.evidence_cards||[]).map(r=>'<article class="evidence"><div class="evidence-top"><h3>'+r.action+'</h3><div class="saving">'+money(r.annual_savings)+'</div></div><p class="small">'+r.math+'</p><p class="small">'+(r.evidence||[]).map(ev=>'<b>'+ev.kind+':</b> '+ev.finding).join('<br>')+'</p>'+tagList(['fee if verified '+money(r.success_fee_if_verified),'risk '+r.risk,'approval required'])+'</article>').join('');
  el('runLog').innerHTML=(e.run_log||[]).map(x=>'<div class="runitem"><b>+'+x.t_plus_sec+'s</b><span>'+x.event+'</span><b class="ok">'+x.status+'</b></div>').join('');
  el('replayBtn').onclick=()=>{document.querySelector('.replay').scrollIntoView({behavior:'smooth'});document.querySelectorAll('.runitem').forEach((n,i)=>{n.style.opacity=.35;setTimeout(()=>{n.style.opacity=1;n.style.borderColor='#86efac'},i*170)})};
})}
boot();setInterval(boot,30000);
