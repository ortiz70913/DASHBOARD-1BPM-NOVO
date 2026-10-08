from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- RELATORIO_INTELIGENCIA_V6 -->'
if marker in s:
    raise SystemExit(0)
js=r'''<!-- RELATORIO_INTELIGENCIA_V6 -->
<style>
#riV6Panel{position:fixed;inset:70px 14px 14px;z-index:100000;background:var(--card,#fff);color:var(--ink,#0f1c2e);border:1px solid var(--line,#dfe5ec);border-radius:14px;box-shadow:0 20px 70px rgba(0,0,0,.45);overflow:auto;padding:18px}
#riV6Panel[hidden]{display:none!important}
#riV6Panel .v6head{display:flex;justify-content:space-between;align-items:center;gap:10px;position:sticky;top:-18px;background:var(--card,#fff);padding:4px 0 12px;z-index:5}
#riV6Panel button{cursor:pointer;border:1px solid var(--line,#dfe5ec);border-radius:8px;padding:9px 13px;background:#17395f;color:#fff!important;font-weight:700}
#riV6Panel select,#riV6Panel input{padding:9px;border:1px solid var(--line,#dfe5ec);border-radius:8px;background:var(--bg,#f4f6f9);color:var(--ink,#0f1c2e)}
#riV6Panel .v6filters{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
#riV6Panel .v6status{padding:10px;margin:8px 0;border-radius:8px;background:var(--bg,#f4f6f9)}
#riV6Panel table{width:100%;border-collapse:collapse;font-size:12px}
#riV6Panel th,#riV6Panel td{border:1px solid var(--line,#dfe5ec);padding:7px;text-align:left;vertical-align:top}
#riV6Panel th{position:sticky;top:50px;background:#17395f;color:#fff;z-index:3}
</style>
<script>
(function(){
'use strict';
var rows=[];
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function cia(v){var s=String(v==null?'':v);if(/^1$|1ª|1a/i.test(s))return '1ª CIA';if(/^2$|2ª|2a/i.test(s))return '2ª CIA';if(/^3$|3ª|3a/i.test(s))return '3ª CIA';return s||'Sem CIA';}
function month(v){if(!v)return 'Sem data';var d=new Date(String(v).slice(0,10)+'T00:00:00');return isNaN(d)?String(v):d.toLocaleDateString('pt-BR',{month:'2-digit',year:'numeric'});}
function db(x){return {data:x.data,cia:x.cia,bairro:x.bairro||'Não informado',local:x.local_fato||'Não informado',logradouro:x.logradouro||'Não informado',hora:x.hora,turno:x.turno,motivacao:x.motivacao||'',arma:x.arma||'Não informado',abordagem:x.abordagem||'',tipo_veiculo:x.tipo_veiculo||'',modelo:x.modelo||'',marca:x.marca||'',estabelecimento:x.estabelecimento||'',modo_acao:x.modo_acao||'',recuperacao:x.recuperacao||'',orcrim_vitima:x.orcrim_vitima||'',orcrim_autor:x.orcrim_autor||''};}
function fallback(){var o=[];try{Object.keys(DS||{}).forEach(function(k){((DS[k]||{}).R||[]).forEach(function(x){o.push({data:x[0],cia:x[1],bairro:x[3]||'Não informado',local:x[9]||'Não informado',logradouro:x[11]||'Não informado',hora:x[5],turno:x[2],motivacao:x[7]||'',arma:x[8]||'Não informado',abordagem:x[10]||'',tipo_veiculo:x[12]||'',modelo:x[13]||'',marca:x[14]||'',estabelecimento:x[16]||'',modo_acao:x[19]||'',recuperacao:x[20]||'',orcrim_vitima:x[25]||'',orcrim_autor:x[26]||''});});});}catch(e){}return o.filter(function(x){return x.data;});}
async function load(){var u=window.SUPABASE_URL,k=window.SUPABASE_ANON_KEY;if(!u||!k)throw Error('Configuração do Supabase não encontrada');var out=[],off=0;while(true){var r=await fetch(u+'/rest/v1/ocorrencias?select=*&order=data.asc&offset='+off+'&limit=1000',{headers:{apikey:k,Authorization:'Bearer '+k}});if(!r.ok)throw Error('Supabase HTTP '+r.status);var a=await r.json();out=out.concat(a);if(a.length<1000)break;off+=1000;if(off>100000)break;}return out.map(db).filter(function(x){return x.data;});}
function ui(){if(document.getElementById('riV6Panel'))return;var p=document.createElement('div');p.id='riV6Panel';p.hidden=true;p.innerHTML='<div class="v6head"><h2>📋 Relatório de Inteligência</h2><button type="button" id="riV6Close">Fechar</button></div><div class="v6filters"><select id="riV6Cia"><option value="">Todas as CIAs</option><option>1ª CIA</option><option>2ª CIA</option><option>3ª CIA</option></select><select id="riV6Month"><option value="">Todos os meses</option></select><input id="riV6Q" placeholder="Pesquisar..."/></div><div id="riV6Status" class="v6status"></div><div id="riV6Body"></div>';document.body.appendChild(p);document.getElementById('riV6Close').onclick=function(){p.hidden=true;};['riV6Cia','riV6Month','riV6Q'].forEach(function(id){document.getElementById(id).addEventListener('input',render);});}
function render(){var c=document.getElementById('riV6Cia').value,m=document.getElementById('riV6Month').value,q=document.getElementById('riV6Q').value.toLowerCase();var a=rows.filter(function(r){return(!c||cia(r.cia)===c)&&(!m||month(r.data)===m)&&(!q||[r.data,cia(r.cia),r.bairro,r.local,r.logradouro,r.motivacao,r.arma,r.abordagem,r.marca,r.modelo,r.estabelecimento,r.modo_acao,r.recuperacao,r.orcrim_vitima,r.orcrim_autor].join(' ').toLowerCase().indexOf(q)>=0);});var months={};rows.forEach(function(r){months[month(r.data)]=1;});var sel=document.getElementById('riV6Month'),old=sel.value;sel.innerHTML='<option value="">Todos os meses</option>'+Object.keys(months).sort().reverse().map(function(x){return '<option>'+esc(x)+'</option>';}).join('');sel.value=old;document.getElementById('riV6Status').textContent='Registros carregados: '+rows.length+' | Exibindo: '+a.length;if(!a.length){document.getElementById('riV6Body').innerHTML='<p>Nenhuma ocorrência encontrada.</p>';return;}document.getElementById('riV6Body').innerHTML='<div style="overflow:auto"><table><thead><tr><th>Data</th><th>CIA</th><th>Hora</th><th>Bairro</th><th>Local</th><th>Logradouro</th><th>Motivação</th><th>Arma</th><th>Abordagem</th><th>Veículo</th><th>Estabelecimento</th><th>Modo de ação</th><th>Recuperação</th></tr></thead><tbody>'+a.slice().sort(function(x,y){return String(y.data).localeCompare(String(x.data));}).map(function(r){return '<tr><td>'+esc(r.data)+'</td><td>'+esc(cia(r.cia))+'</td><td>'+esc(r.hora)+'</td><td>'+esc(r.bairro)+'</td><td>'+esc(r.local)+'</td><td>'+esc(r.logradouro)+'</td><td>'+esc(r.motivacao)+'</td><td>'+esc(r.arma)+'</td><td>'+esc(r.abordagem)+'</td><td>'+esc([r.marca,r.modelo,r.tipo_veiculo].filter(Boolean).join(' / '))+'</td><td>'+esc(r.estabelecimento)+'</td><td>'+esc(r.modo_acao)+'</td><td>'+esc(r.recuperacao)+'</td></tr>';}).join('')+'</tbody></table></div>';}
async function open(e){if(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();}ui();var p=document.getElementById('riV6Panel');p.hidden=false;document.getElementById('riV6Status').textContent='Carregando ocorrências...';try{rows=await load();}catch(err){rows=fallback();if(!rows.length){document.getElementById('riV6Status').textContent='Erro: '+err.message;return;}}render();}
function install(){ui();var found=[].slice.call(document.querySelectorAll('button,a,[role="button"]')).filter(function(x){return /Relat.rio de Intelig.ncia/i.test(x.textContent||'')&&!x.id.match(/^riV6Button$/);});found.forEach(function(old){var b=document.createElement('button');b.type='button';b.id='riV6Button';b.textContent='📋 Relatório de Inteligência';b.title='Abrir Relatório de Inteligência';b.style.cssText='display:inline-block!important;visibility:visible!important;opacity:1!important;color:#fff!important;background:#17395f!important;cursor:pointer!important;font-weight:700!important;';b.dataset.riV5Bound='1';b.addEventListener('click',open,true);old.parentNode.replaceChild(b,old);});var b=document.getElementById('riV6Button');if(b&&!b.dataset.riV6Bound){b.dataset.riV6Bound='1';b.addEventListener('click',open,true);}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(install,500);});else setTimeout(install,500);setInterval(install,1000);
})();
</script>
'''
s=s.replace('</body>',js+'</body>')
p.write_text(s,encoding='utf-8')
