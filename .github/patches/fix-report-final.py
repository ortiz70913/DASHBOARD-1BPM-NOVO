from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove todas as versões anteriores do relatório injetadas no HTML.
s = re.sub(r'/\* RELATORIO_INTELIGENCIA_PATCH_V2 \*/.*?(?=<!-- RELATORIO_INTELIGENCIA_V5 -->)', '', s, flags=re.S)
s = re.sub(r'<!-- RELATORIO_INTELIGENCIA_V5 -->.*?(?=</body>)', '', s, flags=re.S)
s = re.sub(r'<!-- RELATORIO_INTELIGENCIA_V7_AUTH -->', '', s)

final_script = r'''<!-- RELATORIO_INTELIGENCIA_FINAL -->
<style>
#riFinalButton{display:inline-flex!important;align-items:center;justify-content:center;margin:6px 4px;padding:9px 12px;border:1px solid rgba(255,255,255,.35);border-radius:9px;background:#17395f;color:#fff!important;font-weight:800;cursor:pointer;min-height:40px}
#riFinalButton::before{content:'📋 Relatório de Inteligência'}
#riFinalButton span{display:none}
#riFinalPanel{position:fixed;inset:70px 14px 14px;z-index:100000;background:var(--card,#fff);color:var(--ink,#0f1c2e);border:1px solid var(--line,#dfe5ec);border-radius:14px;box-shadow:0 20px 70px rgba(0,0,0,.45);overflow:auto;padding:18px}
#riFinalPanel[hidden]{display:none!important}
#riFinalPanel .rif-head{display:flex;align-items:center;justify-content:space-between;gap:12px;position:sticky;top:-18px;background:var(--card,#fff);padding:4px 0 12px;z-index:5}
#riFinalPanel h2{margin:0;font-size:20px}
#riFinalPanel button{cursor:pointer;border:1px solid var(--line,#dfe5ec);border-radius:8px;padding:9px 13px;background:#17395f;color:#fff;font-weight:700}
#riFinalPanel .rif-filters{display:grid;grid-template-columns:180px 180px 1fr;gap:8px;margin:8px 0 12px}
#riFinalPanel select,#riFinalPanel input{width:100%;padding:9px;border:1px solid var(--line,#dfe5ec);border-radius:8px;background:var(--card,#fff);color:var(--ink,#0f1c2e)}
#riFinalPanel .rif-status{padding:10px 12px;border-radius:8px;background:var(--bg,#f4f6f9);margin-bottom:12px;font-weight:700}
#riFinalPanel table{width:100%;border-collapse:collapse;font-size:12px}
#riFinalPanel th,#riFinalPanel td{padding:7px;border-bottom:1px solid var(--line,#dfe5ec);text-align:left;white-space:nowrap}
#riFinalPanel th{position:sticky;top:58px;background:var(--card,#fff);z-index:3}
#riFinalPanel .rif-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:12px}
#riFinalPanel .rif-kpi{border:1px solid var(--line,#dfe5ec);border-radius:8px;padding:10px;background:var(--bg,#f4f6f9)}
#riFinalPanel .rif-kpi b{display:block;font-size:20px}
@media(max-width:800px){#riFinalPanel .rif-filters{grid-template-columns:1fr}#riFinalPanel .rif-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
<script>
(function(){
  'use strict';
  var rows=[];
  function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function cia(v){var s=String(v==null?'':v);if(/^1$|1ª|1a/i.test(s))return '1ª CIA';if(/^2$|2ª|2a/i.test(s))return '2ª CIA';if(/^3$|3ª|3a/i.test(s))return '3ª CIA';return s||'Sem CIA';}
  function month(v){if(!v)return 'Sem data';var d=new Date(String(v).slice(0,10)+'T00:00:00');return isNaN(d)?String(v):d.toLocaleDateString('pt-BR',{month:'2-digit',year:'numeric'});}
  function collect(){
    var out=[];
    if(typeof DS==='object'&&DS){Object.keys(DS).forEach(function(k){var a=DS[k]&&DS[k].R||[];a.forEach(function(x){if(!x||!x[0])return;out.push({data:x[0],cia:x[1],turno:x[2],bairro:x[3]||'Não informado',dia:x[4]||'',hora:x[5],presos:x[6]||'',motivacao:x[7]||'',arma:x[8]||'Não informado',local:x[9]||'Não informado',abordagem:x[10]||'',logradouro:x[11]||'Não informado',tipo_veiculo:x[12]||'',modelo:x[13]||'',marca:x[14]||'',estabelecimento:x[16]||'',tipo_roubo:x[17]||'',material:x[18]||'',modo_acao:x[19]||'',recuperacao:x[20]||'',tipo_local:x[22]||'',empresa:x[23]||'',linha:x[24]||'',orcrim_vitima:x[25]||'',orcrim_autor:x[26]||''});});});}
    return out;
  }
  function ensure(){
    if(document.getElementById('riFinalPanel'))return;
    var p=document.createElement('section');p.id='riFinalPanel';p.hidden=true;p.innerHTML='<div class="rif-head"><div><h2>📋 Relatório de Inteligência</h2><div>Dados da mesma base utilizada pela Análise de Inteligência.</div></div><button id="riFinalClose" type="button">Fechar</button></div><div class="rif-filters"><select id="riFinalCia"><option value="">Todas as CIAs</option><option>1ª CIA</option><option>2ª CIA</option><option>3ª CIA</option></select><select id="riFinalMonth"><option value="">Todos os meses</option></select><input id="riFinalSearch" placeholder="Pesquisar bairro, local, arma, motivação..."/></div><div class="rif-status" id="riFinalStatus">Aguardando carregamento...</div><div class="rif-kpis" id="riFinalKpis"></div><div id="riFinalBody"></div>';
    document.body.appendChild(p);
    document.getElementById('riFinalClose').onclick=function(){p.hidden=true;};
    ['riFinalCia','riFinalMonth','riFinalSearch'].forEach(function(id){document.getElementById(id).addEventListener('input',render);});
  }
  function render(){
    var c=document.getElementById('riFinalCia').value,m=document.getElementById('riFinalMonth').value,q=document.getElementById('riFinalSearch').value.toLowerCase().trim();
    var filtered=rows.filter(function(r){return(!c||cia(r.cia)===c)&&(!m||month(r.data)===m)&&(!q||[r.data,cia(r.cia),r.bairro,r.local,r.logradouro,r.motivacao,r.arma,r.abordagem,r.marca,r.modelo,r.estabelecimento,r.modo_acao,r.recuperacao,r.orcrim_vitima,r.orcrim_autor].join(' ').toLowerCase().indexOf(q)>=0);});
    var months={};rows.forEach(function(r){months[month(r.data)]=1;});
    var sel=document.getElementById('riFinalMonth'),old=sel.value;sel.innerHTML='<option value="">Todos os meses</option>'+Object.keys(months).sort().reverse().map(function(x){return '<option value="'+esc(x)+'">'+esc(x)+'</option>';}).join('');sel.value=old;
    var bairros={};filtered.forEach(function(r){bairros[r.bairro]=(bairros[r.bairro]||0)+1;});var top=Object.keys(bairros).sort(function(a,b){return bairros[b]-bairros[a];})[0]||'—';
    document.getElementById('riFinalStatus').textContent='Registros disponíveis: '+rows.length+' | Exibindo: '+filtered.length;
    document.getElementById('riFinalKpis').innerHTML='<div class="rif-kpi">Total exibido<b>'+filtered.length+'</b></div><div class="rif-kpi">1ª CIA<b>'+filtered.filter(function(r){return cia(r.cia)==='1ª CIA';}).length+'</b></div><div class="rif-kpi">2ª CIA<b>'+filtered.filter(function(r){return cia(r.cia)==='2ª CIA';}).length+'</b></div><div class="rif-kpi">3ª CIA<b>'+filtered.filter(function(r){return cia(r.cia)==='3ª CIA';}).length+'</b></div>';
    if(!filtered.length){document.getElementById('riFinalBody').innerHTML='<p>Nenhuma ocorrência encontrada para os filtros selecionados.</p>';return;}
    filtered.sort(function(a,b){return String(b.data).localeCompare(String(a.data));});
    document.getElementById('riFinalBody').innerHTML='<div style="overflow:auto"><table><thead><tr><th>Data</th><th>CIA</th><th>Hora</th><th>Bairro</th><th>Local</th><th>Logradouro</th><th>Motivação</th><th>Arma</th><th>Abordagem</th><th>Veículo</th><th>Estabelecimento</th><th>Modo de ação</th><th>Recuperação</th><th>ORCRIM vítima</th><th>ORCRIM autor</th></tr></thead><tbody>'+filtered.map(function(r){return '<tr><td>'+esc(r.data)+'</td><td>'+esc(cia(r.cia))+'</td><td>'+esc(r.hora)+'</td><td>'+esc(r.bairro)+'</td><td>'+esc(r.local)+'</td><td>'+esc(r.logradouro)+'</td><td>'+esc(r.motivacao)+'</td><td>'+esc(r.arma)+'</td><td>'+esc(r.abordagem)+'</td><td>'+esc([r.marca,r.modelo,r.tipo_veiculo].filter(Boolean).join(' / '))+'</td><td>'+esc(r.estabelecimento)+'</td><td>'+esc(r.modo_acao)+'</td><td>'+esc(r.recuperacao)+'</td><td>'+esc(r.orcrim_vitima)+'</td><td>'+esc(r.orcrim_autor)+'</td></tr>';}).join('')+'</tbody></table></div>';
  }
  async function openReport(e){if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation();}ensure();var p=document.getElementById('riFinalPanel');p.hidden=false;document.getElementById('riFinalStatus').textContent='Atualizando dados da mesma fonte do dashboard...';try{if(typeof loadData==='function'){await loadData();}rows=collect();if(!rows.length){document.getElementById('riFinalStatus').textContent='A consulta foi executada, mas não há registros disponíveis para o relatório.';document.getElementById('riFinalBody').innerHTML='';document.getElementById('riFinalKpis').innerHTML='';return;}render();}catch(err){document.getElementById('riFinalStatus').textContent='Erro ao carregar dados: '+(err&&err.message?err.message:err);document.getElementById('riFinalBody').innerHTML='';}}
  function install(){
    ensure();
    var old=document.getElementById('riFinalButton');
    if(old)return;
    var b=document.createElement('button');b.id='riFinalButton';b.type='button';b.setAttribute('aria-label','Relatório de Inteligência');b.innerHTML='<span>Relatório</span>';b.addEventListener('click',openReport,true);
    var ana=[].slice.call(document.querySelectorAll('button')).find(function(x){return /An.lise de Intelig.ncia/i.test(x.textContent||'');});
    if(ana&&ana.parentNode)ana.parentNode.insertBefore(b,ana.nextSibling);else{var host=document.getElementById('dsb')||document.querySelector('header')||document.body;host.appendChild(b);}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(install,500);});else setTimeout(install,500);
})();
</script>
'''

s = s.replace('</body>', final_script + '</body>')
p.write_text(s, encoding='utf-8')
