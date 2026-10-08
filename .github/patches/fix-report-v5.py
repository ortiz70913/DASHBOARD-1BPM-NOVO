from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- RELATORIO_INTELIGENCIA_V5 -->'
if marker in s:
    raise SystemExit(0)
js=r'''<!-- RELATORIO_INTELIGENCIA_V5 -->
<style>
#riV5Panel{position:fixed;inset:72px 18px 18px;z-index:99999;background:var(--card,#fff);color:var(--ink,#0f1c2e);border:1px solid var(--line,#dfe5ec);border-radius:14px;box-shadow:0 18px 60px rgba(0,0,0,.35);overflow:auto;padding:18px}
#riV5Panel[hidden]{display:none!important}
#riV5Panel .ri-head{display:flex;align-items:center;justify-content:space-between;gap:12px;position:sticky;top:-18px;padding:4px 0 14px;background:var(--card,#fff);z-index:2}
#riV5Panel h2{margin:0;font-size:20px}
#riV5Panel .ri-close,#riV5Button{cursor:pointer;border:1px solid var(--line,#dfe5ec);border-radius:8px;padding:9px 14px;background:#17395f;color:#fff!important;font-weight:700}
#riV5Panel .ri-filters{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 14px}
#riV5Panel select,#riV5Panel input{padding:9px;border:1px solid var(--line,#dfe5ec);border-radius:8px;background:var(--bg,#f4f6f9);color:var(--ink,#0f1c2e)}
#riV5Panel .ri-status{padding:10px;border-radius:8px;margin:8px 0;background:var(--bg,#f4f6f9)}
#riV5Panel .ri-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}
#riV5Panel .ri-card{padding:12px;border:1px solid var(--line,#dfe5ec);border-radius:10px;background:var(--bg,#f4f6f9)}
#riV5Panel .ri-card b{display:block;font-size:22px}
#riV5Panel .ri-table{width:100%;border-collapse:collapse;font-size:12px}
#riV5Panel .ri-table th,#riV5Panel .ri-table td{border:1px solid var(--line,#dfe5ec);padding:7px;text-align:left;vertical-align:top}
#riV5Panel .ri-table th{position:sticky;top:51px;background:#17395f;color:#fff;z-index:1}
#riV5Panel .ri-empty{text-align:center;padding:35px;font-weight:600}
@media(max-width:800px){#riV5Panel{inset:55px 6px 6px;padding:10px}.ri-table{font-size:11px}}
</style>
<script>
(function(){
  'use strict';
  function esc(v){return String(v==null?'':v).replace(/[&<>\"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c];});}
  function ciaLabel(v){if(v==null||v==='')return 'Sem CIA';var n=String(v);if(/^1$|1ª|1a/i.test(n))return '1ª CIA';if(/^2$|2ª|2a/i.test(n))return '2ª CIA';if(/^3$|3ª|3a/i.test(n))return '3ª CIA';return n;}
  function monthLabel(d){if(!d)return 'Sem data';var x=new Date(d+'T00:00:00');if(isNaN(x))return String(d);return x.toLocaleDateString('pt-BR',{month:'2-digit',year:'numeric'});}
  function getVal(x,k){return x[k]==null?'':x[k];}
  function rowFromDb(x){return {data:getVal(x,'data'),cia:getVal(x,'cia'),bairro:getVal(x,'bairro')||'Não informado',local:getVal(x,'local_fato')||'Não informado',logradouro:getVal(x,'logradouro')||'Não informado',hora:getVal(x,'hora'),turno:getVal(x,'turno'),motivacao:getVal(x,'motivacao'),arma:getVal(x,'arma')||'Não informado',abordagem:getVal(x,'abordagem'),tipo_veiculo:getVal(x,'tipo_veiculo'),modelo:getVal(x,'modelo'),marca:getVal(x,'marca'),estabelecimento:getVal(x,'estabelecimento'),tipo_roubo:getVal(x,'tipo_roubo'),material:getVal(x,'material'),modo_acao:getVal(x,'modo_acao'),recuperacao:getVal(x,'recuperacao'),tipo_local:getVal(x,'tipo_local'),empresa:getVal(x,'empresa'),linha:getVal(x,'linha'),orcrim_vitima:getVal(x,'orcrim_vitima'),orcrim_autor:getVal(x,'orcrim_autor')};}
  async function fetchRows(){
    var url=window.SUPABASE_URL,key=window.SUPABASE_ANON_KEY;
    if(!url||!key)throw new Error('Configuração do Supabase não encontrada.');
    var all=[],offset=0,size=1000;
    while(true){
      var endpoint=url+'/rest/v1/ocorrencias?select=*&order=data.asc&offset='+offset+'&limit='+size;
      var r=await fetch(endpoint,{headers:{apikey:key,Authorization:'Bearer '+key}});
      if(!r.ok){var txt=await r.text();throw new Error('Supabase HTTP '+r.status+(txt?' — '+txt.slice(0,180):''));}
      var a=await r.json();
      if(!Array.isArray(a))throw new Error('Resposta inválida do Supabase.');
      all=all.concat(a);
      if(a.length<size)break;
      offset+=size;
      if(offset>100000)break;
    }
    return all.map(rowFromDb).filter(function(r){return r.data;});
  }
  function fallbackRows(){
    var out=[];
    try{if(typeof DS==='object')Object.keys(DS).forEach(function(k){var a=DS[k]&&DS[k].R||[];a.forEach(function(x){out.push({data:x[0],cia:x[1],bairro:x[3]||'Não informado',local:x[9]||'Não informado',logradouro:x[11]||'Não informado',hora:x[5],turno:x[2],motivacao:x[7],arma:x[8]||'Não informado',abordagem:x[10],tipo_veiculo:x[12],modelo:x[13],marca:x[14],estabelecimento:x[16],tipo_roubo:x[17],material:x[18],modo_acao:x[19],recuperacao:x[20],tipo_local:x[22],empresa:x[23],linha:x[24],orcrim_vitima:x[25],orcrim_autor:x[26]});});});}catch(e){}
    return out.filter(function(r){return r.data;});
  }
  var rows=[];
  function ensureUI(){
    var old=document.getElementById('riV5Panel');if(old)return;
    var panel=document.createElement('div');panel.id='riV5Panel';panel.hidden=true;panel.innerHTML='<div class="ri-head"><h2>📋 Relatório de Inteligência</h2><button class="ri-close" type="button">Fechar</button></div><div class="ri-filters"><select id="riV5Cia"><option value="">Todas as CIAs</option><option>1ª CIA</option><option>2ª CIA</option><option>3ª CIA</option></select><select id="riV5Month"><option value="">Todos os meses</option></select><input id="riV5Search" placeholder="Pesquisar bairro, local, arma..."/></div><div id="riV5Status" class="ri-status">Carregando dados...</div><div id="riV5Body"></div>';
    document.body.appendChild(panel);
    panel.querySelector('.ri-close').onclick=function(){panel.hidden=true;};
    ['riV5Cia','riV5Month','riV5Search'].forEach(function(id){panel.querySelector('#'+id).addEventListener('input',render);});
  }
  function render(){
    var cia=document.getElementById('riV5Cia').value,mon=document.getElementById('riV5Month').value,q=document.getElementById('riV5Search').value.trim().toLowerCase();
    var a=rows.filter(function(r){var text=[r.data,ciaLabel(r.cia),r.bairro,r.local,r.logradouro,r.arma,r.motivacao,r.abordagem,r.estabelecimento,r.material,r.orcrim_vitima,r.orcrim_autor].join(' ').toLowerCase();return (!cia||ciaLabel(r.cia)===cia)&&(!mon||monthLabel(r.data)===mon)&&(!q||text.indexOf(q)>=0);});
    var months={};rows.forEach(function(r){months[monthLabel(r.data)]=1;});
    var ms=document.getElementById('riV5Month'),cur=ms.value;ms.innerHTML='<option value="">Todos os meses</option>'+Object.keys(months).sort().reverse().map(function(m){return '<option>'+esc(m)+'</option>';}).join('');ms.value=cur;
    document.getElementById('riV5Status').textContent='Dados carregados: '+rows.length+' ocorrências | Exibindo: '+a.length;
    var body=document.getElementById('riV5Body');
    if(!a.length){body.innerHTML='<div class="ri-empty">Nenhuma ocorrência encontrada para os filtros selecionados.</div>';return;}
    var bairros={};a.forEach(function(r){bairros[r.bairro]=(bairros[r.bairro]||0)+1;});var top=Object.keys(bairros).sort(function(x,y){return bairros[y]-bairros[x];})[0]||'-';
    body.innerHTML='<div class="ri-cards"><div class="ri-card"><span>Ocorrências</span><b>'+a.length+'</b></div><div class="ri-card"><span>Principal bairro</span><b>'+esc(top)+'</b></div><div class="ri-card"><span>CIAs presentes</span><b>'+Object.keys(a.reduce(function(o,r){o[ciaLabel(r.cia)]=1;return o;},{})).length+'</b></div></div><div style="overflow:auto"><table class="ri-table"><thead><tr><th>Data</th><th>CIA</th><th>Hora</th><th>Bairro</th><th>Local</th><th>Logradouro</th><th>Motivação</th><th>Arma</th><th>Abordagem</th><th>Veículo</th><th>Estabelecimento</th><th>Modo de ação</th><th>Recuperação</th></tr></thead><tbody>'+a.slice().sort(function(x,y){return String(y.data).localeCompare(String(x.data));}).map(function(r){return '<tr><td>'+esc(r.data)+'</td><td>'+esc(ciaLabel(r.cia))+'</td><td>'+esc(r.hora)+'</td><td>'+esc(r.bairro)+'</td><td>'+esc(r.local)+'</td><td>'+esc(r.logradouro)+'</td><td>'+esc(r.motivacao)+'</td><td>'+esc(r.arma)+'</td><td>'+esc(r.abordagem)+'</td><td>'+esc([r.marca,r.modelo,r.tipo_veiculo].filter(Boolean).join(' / '))+'</td><td>'+esc(r.estabelecimento)+'</td><td>'+esc(r.modo_acao)+'</td><td>'+esc(r.recuperacao)+'</td></tr>';}).join('')+'</tbody></table></div>';
  }
  async function openReport(e){
    if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation();}
    ensureUI();var panel=document.getElementById('riV5Panel');panel.hidden=false;
    document.getElementById('riV5Status').textContent='Consultando ocorrências no Supabase...';
    try{rows=await fetchRows();}catch(err){rows=fallbackRows();if(!rows.length){document.getElementById('riV5Status').textContent='ERRO AO CARREGAR: '+err.message;document.getElementById('riV5Body').innerHTML='<div class="ri-empty">'+esc(err.message)+'</div>';return;}}
    render();
  }
  function install(){
    ensureUI();
    var candidates=[].slice.call(document.querySelectorAll('button,a,[role="button"]')).filter(function(el){return /Relat.rio de Intelig.ncia/i.test(el.textContent||'');});
    candidates.forEach(function(el){el.style.setProperty('color','#fff','important');el.style.setProperty('opacity','1','important');el.style.setProperty('visibility','visible','important');if(!el.dataset.riV5Bound){el.dataset.riV5Bound='1';el.addEventListener('click',openReport,true);}});
    if(!document.getElementById('riV5Button')){
      var b=document.createElement('button');b.id='riV5Button';b.type='button';b.textContent='📋 Relatório de Inteligência';b.title='Abrir Relatório de Inteligência';b.addEventListener('click',openReport,true);
      var ana=[].slice.call(document.querySelectorAll('button,a,[role="button"]')).find(function(el){return /An.lise de Intelig.ncia/i.test(el.textContent||'');});
      if(ana&&ana.parentNode)ana.parentNode.insertBefore(b,ana.nextSibling);else document.body.appendChild(b);
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(install,300);});else setTimeout(install,300);
  setInterval(install,1500);
})();
</script>
'''
s=s.replace('</body>',js+'</body>')
p.write_text(s,encoding='utf-8')
