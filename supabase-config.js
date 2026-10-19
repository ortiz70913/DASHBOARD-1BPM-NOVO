window.SUPABASE_URL = 'https://rbpuatcdlbfqxfkbvgst.supabase.co';
window.SUPABASE_ANON_KEY = 'sb_publishable_AH0rCyKZ4J5SMfMwof3TkA_wkTXeg9D';
window.p6 = null;

/* Carrega o Supabase de forma síncrona antes do código principal do Dashboard. */
(function(){
  if(window.supabase && typeof window.supabase.createClient==='function') return;
  document.write('<script src="https://unpkg.com/@supabase/supabase-js@2/dist/umd/supabase.min.js"><\/script>');
})();

/* Inicializa o cliente global usado pelo fluxo de login. */
(function(){
  function initSupabaseClient(){
    try{
      if(window.sb) return true;
      if(!window.supabase || typeof window.supabase.createClient!=='function') return false;
      if(!window.SUPABASE_URL || !window.SUPABASE_ANON_KEY) return false;
      window.sb=window.supabase.createClient(window.SUPABASE_URL,window.SUPABASE_ANON_KEY);
      return !!window.sb;
    }catch(e){
      console.error('Erro ao inicializar cliente Supabase:',e);
      return false;
    }
  }
  if(!initSupabaseClient()){
    var tries=0;
    var timer=setInterval(function(){
      tries++;
      if(initSupabaseClient() || tries>=30) clearInterval(timer);
    },100);
  }
})();

/* AJUSTE DIRETO DOS GRAFICOS - nome e barra proporcionais ao espaco real */
(function(){
  const style=document.createElement('style');
  style.id='dashboard-chart-layout-final-v9';
  style.textContent=`
    .bars{display:flex!important;flex-direction:column!important;width:100%!important;max-width:100%!important;gap:5px!important;padding:0!important;margin:0!important;box-sizing:border-box!important}
    .bars .bar{display:grid!important;grid-template-columns:fit-content(220px) minmax(0,1fr)!important;grid-template-rows:26px 12px!important;column-gap:5px!important;row-gap:1px!important;width:100%!important;min-width:0!important;height:auto!important;min-height:0!important;padding:1px 0!important;margin:0!important;align-items:center!important;box-sizing:border-box!important}
    .bars .bar>b{grid-column:1!important;grid-row:1 / span 2!important;display:flex!important;align-items:center!important;gap:5px!important;width:auto!important;max-width:220px!important;min-width:0!important;height:39px!important;overflow:hidden!important;white-space:nowrap!important;text-overflow:ellipsis!important;font-size:.84rem!important;line-height:1.1!important}
    .bars .bar>div{grid-column:2!important;grid-row:1!important;position:relative!important;width:100%!important;min-width:0!important;height:24px!important;min-height:24px!important;margin:0!important;box-sizing:border-box!important}
    .bars .bar .bardelta{grid-column:2!important;grid-row:2!important;width:100%!important;height:12px!important;min-height:0!important;margin:0!important;padding:0!important;line-height:12px!important;font-size:.60rem!important;white-space:nowrap!important}
    .bars .bar>b .ranknum{flex:0 0 auto!important;min-width:27px!important;height:23px!important}

    #p-faixas .bars .bar,#p-dia-faixa .bars .bar,#p-companhia .bars .bar,#p-motivacao .bars .bar,#p-local .bars .bar,#p-orcrim-vitima .bars .bar,#p-orcrim-autores .bars .bar,#p-bairro .bars .bar{grid-template-columns:fit-content(220px) minmax(0,1fr)!important;column-gap:5px!important}
    #p-faixas .bars .bar>b,#p-dia-faixa .bars .bar>b,#p-companhia .bars .bar>b,#p-motivacao .bars .bar>b,#p-local .bars .bar>b,#p-orcrim-vitima .bars .bar>b,#p-orcrim-autores .bars .bar>b,#p-bairro .bars .bar>b{width:auto!important;max-width:220px!important}

    .critical-item{display:grid!important;grid-template-columns:34px max-content minmax(0,1fr) 32px!important;column-gap:3px!important;row-gap:0!important;width:100%!important;min-width:0!important;align-items:center!important}
    .critical-item .pos{grid-column:1!important;width:34px!important;min-width:34px!important;margin:0!important;padding:0!important}
    .critical-item .name{grid-column:2!important;width:max-content!important;max-width:260px!important;min-width:0!important;margin:0!important;padding:0!important;overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important}
    .critical-item .bar{grid-column:3!important;width:100%!important;min-width:0!important;margin:0!important;padding:0!important}
    .critical-item .val{grid-column:4!important;width:32px!important;min-width:32px!important;margin:0!important;padding:0!important;text-align:right!important}

    .rankitem{display:grid!important;grid-template-columns:34px max-content minmax(0,1fr) 34px!important;column-gap:5px!important;row-gap:0!important;width:100%!important;min-width:0!important;align-items:center!important}
    .rankitem .pos{grid-column:1!important;width:34px!important;min-width:34px!important;margin:0!important;padding:0!important}
    .rankitem .name{grid-column:2!important;width:max-content!important;max-width:320px!important;min-width:0!important;margin:0!important;padding:0!important;overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important}
    .rankitem .bar{grid-column:3!important;width:100%!important;min-width:0!important;margin:0!important;padding:0!important}
    .rankitem .val{grid-column:4!important;width:34px!important;min-width:34px!important;margin:0!important;padding:0!important;text-align:right!important}

    #p-cia .ciarow{width:100%!important;margin:2px 0 6px!important}
    #p-cia .ciarow .hb{display:grid!important;grid-template-columns:105px minmax(0,1fr) 86px!important;gap:7px!important;align-items:center!important;width:100%!important;margin:5px 0!important;padding:0!important}
    #p-cia .ciarow .hbname{min-width:0!important;overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important;font-weight:700!important}
    #p-cia .ciarow .hb div{height:14px!important;min-width:0!important;width:100%!important;background:#e7edf4!important;border-radius:7px!important;overflow:hidden!important;box-shadow:none!important}
    #p-cia .ciarow .hb div i{display:block!important;height:100%!important;min-width:3px!important;background:linear-gradient(90deg,var(--acc),var(--hi))!important;border-radius:7px!important}
    #p-cia .ciarow .hb b{font-size:.80rem!important;text-align:right!important;white-space:nowrap!important}

    #p-motiv .bars,#p-bairro .bars{width:100%!important;margin:2px 0 0!important;gap:6px!important}
    #p-motiv .bars .bar,#p-bairro .bars .bar{display:grid!important;grid-template-columns:fit-content(240px) minmax(0,1fr)!important;grid-template-rows:24px 12px!important;column-gap:7px!important;row-gap:1px!important;width:100%!important;min-height:0!important;height:auto!important;margin:0!important;padding:1px 0!important}
    #p-motiv .bars .bar>b,#p-bairro .bars .bar>b{grid-column:1!important;grid-row:1 / span 2!important;max-width:240px!important;width:auto!important;height:37px!important;font-size:.82rem!important;line-height:1.1!important}
    #p-motiv .bars .bar>div,#p-bairro .bars .bar>div{grid-column:2!important;grid-row:1!important;width:100%!important;height:20px!important;min-height:20px!important;background:#e7edf4!important;border-radius:7px!important;overflow:hidden!important;position:relative!important}
    #p-motiv .bars .bar>div>i,#p-bairro .bars .bar>div>i{display:block!important;height:100%!important;min-width:3px!important;background:linear-gradient(90deg,var(--acc),var(--hi))!important;border-radius:7px!important}
    #p-motiv .bars .bar>div>em,#p-bairro .bars .bar>div>em{position:absolute!important;right:7px!important;top:50%!important;transform:translateY(-50%)!important;font-style:normal!important;font-size:.68rem!important;font-weight:800!important;color:var(--ink)!important;white-space:nowrap!important;z-index:2!important}
    #p-motiv .bars .bar .bardelta,#p-bairro .bars .bar .bardelta{grid-column:2!important;grid-row:2!important;width:100%!important;height:11px!important;line-height:11px!important;margin:0!important;padding:0!important;font-size:.57rem!important}

    #p-bairro .bars{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;column-gap:24px!important;row-gap:5px!important;align-items:start!important}
    #p-bairro .bars .bar{width:100%!important}

    @media(max-width:900px){
      .bars .bar{grid-template-columns:fit-content(180px) minmax(0,1fr)!important;column-gap:4px!important}
      .bars .bar>b{width:auto!important;max-width:180px!important}
      .critical-item{grid-template-columns:30px max-content minmax(0,1fr) 28px!important;column-gap:3px!important}
      .critical-item .pos{width:30px!important;min-width:30px!important}.critical-item .name{max-width:210px!important}.critical-item .val{width:28px!important;min-width:28px!important}
      .rankitem{grid-template-columns:30px max-content minmax(0,1fr) 30px!important;column-gap:4px!important}.rankitem .pos{width:30px!important;min-width:30px!important}.rankitem .name{max-width:220px!important}.rankitem .val{width:30px!important;min-width:30px!important}
      #p-cia .ciarow .hb{grid-template-columns:90px minmax(0,1fr) 78px!important}
      #p-motiv .bars .bar,#p-bairro .bars .bar{grid-template-columns:fit-content(200px) minmax(0,1fr)!important}
      #p-motiv .bars .bar>b,#p-bairro .bars .bar>b{max-width:200px!important}
    }
    @media(max-width:600px){
      .bars .bar{grid-template-columns:1fr!important;grid-template-rows:22px 22px 11px!important;gap:2px!important;padding:1px 0!important}
      .bars .bar>b{grid-column:1!important;grid-row:1!important;width:100%!important;height:22px!important;max-width:100%!important}
      .bars .bar>div{grid-column:1!important;grid-row:2!important;width:100%!important;height:22px!important;min-height:22px!important}
      .bars .bar .bardelta{grid-column:1!important;grid-row:3!important;width:100%!important;height:11px!important;line-height:11px!important;margin-left:27px!important}
      .critical-item{grid-template-columns:28px max-content minmax(0,1fr) 26px!important;column-gap:2px!important}.critical-item .pos{width:28px!important;min-width:28px!important}.critical-item .name{max-width:150px!important}.critical-item .val{width:26px!important;min-width:26px!important}
      .rankitem{grid-template-columns:28px max-content minmax(0,1fr) 28px!important;column-gap:3px!important}.rankitem .pos{width:28px!important;min-width:28px!important}.rankitem .name{max-width:150px!important}.rankitem .val{width:28px!important;min-width:28px!important}
      #p-bairro .bars{grid-template-columns:1fr!important;column-gap:0!important}
      #p-cia .ciarow .hb{grid-template-columns:76px minmax(0,1fr) 72px!important;gap:5px!important}
      #p-motiv .bars .bar,#p-bairro .bars .bar{grid-template-columns:fit-content(150px) minmax(0,1fr)!important;column-gap:5px!important}
      #p-motiv .bars .bar>b,#p-bairro .bars .bar>b{max-width:150px!important}
    }
  `;
  document.head.appendChild(style);
})();

(function(){
  function fixMonthlyChart(){
    const root=document.getElementById('mes');
    if(!root)return;
    const cols=root.querySelector(':scope > .cols');
    const lab=root.querySelector(':scope > .lab');
    if(cols && lab){
      const labels=[...lab.children].map(x=>x.textContent.trim());
      [...cols.children].forEach((col,i)=>{
        let tag=col.querySelector('.month-label');
        if(!tag){tag=document.createElement('span');tag.className='month-label';col.appendChild(tag)}
        tag.textContent=labels[i]||'';
      });
      lab.remove();
      root.classList.add('monthly-chart-fixed');
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fixMonthlyChart,{once:true});else setTimeout(fixMonthlyChart,0);
  new MutationObserver(fixMonthlyChart).observe(document.documentElement,{childList:true,subtree:true});
})();