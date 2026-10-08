/* RELATORIO_INTELIGENCIA_REAL_V3 */
(function(){
'use strict';
var OPEN=/Relat.rio\s+de\s+Intelig.ncia/i;
var panelId='relatorioInteligenciaReal';
var reportClient=null;
function esc(v){return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#39;')}
function first(o,keys){for(var i=0;i<keys.length;i++){if(o&&o[keys[i]]!=null&&o[keys[i]]!=='')return o[keys[i]]}return ''}
function dateBR(v){if(!v)return '';var s=String(v),p=s.slice(0,10).split('-');return p.length===3?p[2]+'/'+p[1]+'/'+p[0]:s}
function getClient(){
 if(reportClient)return reportClient;
 if(!window.supabase)throw new Error('Biblioteca do Supabase não foi carregada.');
 var url=window.SUPABASE_URL||'';
 var key=window.SUPABASE_ANON_KEY||'';
 if(!url||!key)throw new Error('Configuração do Supabase não encontrada.');
 reportClient=window.supabase.createClient(url,key);
 return reportClient;
}
function panel(){var p=document.getElementById(panelId);if(p)return p;p=document.createElement('div');p.id=panelId;p.style.cssText='position:fixed;inset:4vh 3vw;z-index:999999;background:#fff;color:#10243a;border:2px solid #315b86;border-radius:12px;box-shadow:0 18px 60px rgba(0,0,0,.45);display:none;overflow:hidden;font-family:Segoe UI,Arial,sans-serif';document.body.appendChild(p);return p}
function show(body){var p=panel();p.style.display='block';p.innerHTML='<div style="padding:14px 18px;background:#0b2545;color:#fff;display:flex;justify-content:space-between;align-items:center"><b>📋 RELATÓRIO DE INTELIGÊNCIA</b><button id="riClose" style="background:#fff;color:#0b2545;border:0;border-radius:6px;padding:6px 12px;cursor:pointer;font-weight:700">Fechar</button></div><div id="riBody" style="padding:18px;overflow:auto;height:calc(100% - 58px)">'+body+'</div>';document.getElementById('riClose').onclick=function(){p.style.display='none'};return p}
async function loadAll(){var client=getClient(),all=[],from=0,page=1000;while(true){var q=await client.from('ocorrencias').select('*').order('data',{ascending:true}).range(from,from+page-1);if(q.error)throw q.error;var rows=q.data||[];all=all.concat(rows);if(rows.length<page)break;from+=page}return all}
function render(rows){var h='<div style="margin-bottom:12px;font-weight:700">Registros encontrados: '+rows.length+'</div>';if(!rows.length)return h+'<div style="padding:20px;border:1px solid #ddd;border-radius:8px">Nenhum registro encontrado na tabela ocorrencias.</div>';h+='<div style="overflow:auto"><table style="border-collapse:collapse;width:100%;font-size:13px;white-space:nowrap"><thead><tr style="background:#eaf0f6">';['Data','CIA','Hora','Bairro','Local','Logradouro','Motivação','Arma','Abordagem','Veículo','Estabelecimento','Modo de ação','Recuperação','ORCRIM'].forEach(function(x){h+='<th style="padding:8px;border:1px solid #d7dee7">'+x+'</th>'});h+='</tr></thead><tbody>';rows.forEach(function(r){h+='<tr>';var vals=[dateBR(r.data),first(r,['cia','Cia','CIA']),first(r,['hora','Hora']),first(r,['bairro','Bairro']),first(r,['local','Local']),first(r,['logradouro','Logradouro','endereco','Endereco']),first(r,['motivacao','Motivacao','motivação']),first(r,['arma','Arma']),first(r,['abordagem','Abordagem']),first(r,['veiculo','Veiculo','veículo']),first(r,['estabelecimento','Estabelecimento']),first(r,['modo_acao','modoacao','modoDeAcao']),first(r,['recuperacao','Recuperacao','recuperação']),first(r,['orcrim','ORCRIM'])];vals.forEach(function(v){h+='<td style="padding:7px;border:1px solid #d7dee7">'+esc(v)+'</td>'});h+='</tr>'});return h+'</tbody></table></div>'}
async function open(e){if(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation()}show('<b>Consultando os dados do Supabase...</b>');try{var rows=await loadAll();document.getElementById('riBody').innerHTML=render(rows)}catch(err){document.getElementById('riBody').innerHTML='<div style="padding:16px;background:#fff1f1;border:1px solid #d66;border-radius:8px"><b>Erro ao carregar os dados:</b><br>'+esc(err&&err.message?err.message:err)+'</div>'}}
document.addEventListener('click',function(e){var b=e.target&&e.target.closest?e.target.closest('button'):null;if(!b)return;var t=(b.textContent||'')+' '+(b.getAttribute('aria-label')||'');if(OPEN.test(t))open(e)},true);
window.openIntelligenceReport=open;
})();