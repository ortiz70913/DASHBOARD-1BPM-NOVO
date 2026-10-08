(function(){
  'use strict';
  var OPEN=/Relat.rio\s+de\s+Intelig.ncia/i;
  var panelId='relatorioInteligenciaReal';
  function esc(v){return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#39;')}
  function pick(o){return o==null?'':String(o)}
  function first(o,keys){for(var i=0;i<keys.length;i++){if(o && o[keys[i]]!=null && o[keys[i]]!=='') return o[keys[i]]}return ''}
  function dateBR(v){if(!v)return '';var s=String(v).slice(0,10);var p=s.split('-');return p.length===3?p[2]+'/'+p[1]+'/'+p[0]:s}
  function getPanel(){var p=document.getElementById(panelId);if(p)return p;p=document.createElement('div');p.id=panelId;p.style.cssText='position:fixed;inset:4vh 3vw;z-index:999999;background:#fff;color:#10243a;border:2px solid #315b86;border-radius:12px;box-shadow:0 18px 60px rgba(0,0,0,.45);display:none;overflow:hidden;font-family:Segoe UI,Arial,sans-serif';document.body.appendChild(p);return p}
  function show(msg){var p=getPanel();p.style.display='block';p.innerHTML='<div style="padding:14px 18px;background:#0b2545;color:#fff;display:flex;justify-content:space-between;align-items:center"><b>📋 RELATÓRIO DE INTELIGÊNCIA</b><button id="riClose" style="background:#fff;color:#0b2545;border:0;border-radius:6px;padding:6px 12px;cursor:pointer;font-weight:700">Fechar</button></div><div style="padding:18px;overflow:auto;height:calc(100% - 58px)">'+msg+'</div>';document.getElementById('riClose').onclick=function(){p.style.display='none'};return p}
  async function loadAll(){
    if(typeof sb==='undefined' || !sb || !sb.from) throw new Error('Conexão com o Supabase não encontrada.');
    var all=[],from=0,page=1000;
    while(true){
      var r=await sb.from('ocorrencias').select('*').order('data',{ascending:true}).range(from,from+page-1);
      if(r.error)throw r.error;
      var rows=r.data||[];all=all.concat(rows);
      if(rows.length<page)break;from+=page;
    }
    return all;
  }
  function render(rows){
    var h='<div style="margin-bottom:12px;font-weight:700">Registros encontrados: '+rows.length+'</div>';
    if(!rows.length)return h+'<div style="padding:20px;border:1px solid #ddd;border-radius:8px">Nenhum registro encontrado na tabela <b>ocorrencias</b>.</div>';
    h+='<div style="overflow:auto;border:1px solid #d7dee7;border-radius:8px"><table style="border-collapse:collapse;width:100%;font-size:13px;white-space:nowrap"><thead><tr style="background:#eaf0f6"><th style="padding:8px;border:1px solid #d7dee7">Data</th><th style="padding:8px;border:1px solid #d7dee7">CIA</th><th style="padding:8px;border:1px solid #d7dee7">Hora</th><th style="padding:8px;border:1px solid #d7dee7">Bairro</th><th style="padding:8px;border:1px solid #d7dee7">Local</th><th style="padding:8px;border:1px solid #d7dee7">Logradouro</th><th style="padding:8px;border:1px solid #d7dee7">Motivação</th><th style="padding:8px;border:1px solid #d7dee7">Arma</th><th style="padding:8px;border:1px solid #d7dee7">Abordagem</th><th style="padding:8px;border:1px solid #d7dee7">Veículo</th><th style="padding:8px;border:1px solid #d7dee7">Estabelecimento</th><th style="padding:8px;border:1px solid #d7dee7">Modo de ação</th><th style="padding:8px;border:1px solid #d7dee7">Recuperação</th><th style="padding:8px;border:1px solid #d7dee7">ORCRIM</th></tr></thead><tbody>';
    rows.forEach(function(r){h+='<tr><td style="padding:7px;border:1px solid #d7dee7">'+esc(dateBR(r.data))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['cia','Cia','CIA']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['hora','Hora']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['bairro','Bairro']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['local','Local']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['logradouro','Logradouro','endereco','Endereco']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['motivacao','Motivacao','motivação']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['arma','Arma']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['abordagem','Abordagem']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['veiculo','Veiculo','veículo']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['estabelecimento','Estabelecimento']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['modo_acao','modoacao','modoDeAcao','modo de ação']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['recuperacao','Recuperacao','recuperação']))+'</td><td style="padding:7px;border:1px solid #d7dee7">'+esc(first(r,['orcrim','ORCRIM']))+'</td></tr>'});
    return h+'</tbody></table></div>';
  }
  async function open(e){if(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation()}var p=show('<div>Consultando os dados de inteligência...</div>');try{var rows=await loadAll();p.querySelector('div[style*="overflow:auto"]');var body=p.children[1];body.innerHTML=render(rows)}catch(err){p.children[1].innerHTML='<div style="padding:16px;background:#fff1f1;border:1px solid #d66;border-radius:8px"><b>Erro ao carregar o relatório:</b><br>'+esc(err&&err.message?err.message:err)+'</div>'}}
  document.addEventListener('click',function(e){var b=e.target&&e.target.closest?e.target.closest('button'):null;if(!b)return;var t=(b.textContent||'')+' '+(b.getAttribute('aria-label')||'');if(OPEN.test(t))open(e)},true);
  window.openIntelligenceReport=open;
})();