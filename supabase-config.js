window.SUPABASE_URL = 'https://rbpuatcdlbfqxfkbvgst.supabase.co';
window.SUPABASE_ANON_KEY = 'sb_publishable_AH0rCyKZ4J5SMfMwof3TkA_wkTXeg9D';
window.p6 = null;

/* AJUSTE FINAL DOS GRAFICOS - nomes e barras realmente proximos */
(function(){
  const style=document.createElement('style');
  style.id='dashboard-chart-layout-final-v4';
  style.textContent=`
    .bars{display:flex!important;flex-direction:column!important;width:100%!important;max-width:100%!important;gap:3px!important;padding:0!important;margin:0!important;box-sizing:border-box!important}
    .bars .bar{display:grid!important;grid-template-columns:150px minmax(0,1fr)!important;grid-template-rows:26px 12px!important;column-gap:4px!important;row-gap:1px!important;width:100%!important;min-width:0!important;height:auto!important;min-height:0!important;padding:1px 0!important;margin:0!important;align-items:center!important;box-sizing:border-box!important}
    .bars .bar>b{grid-column:1!important;grid-row:1 / span 2!important;display:flex!important;align-items:center!important;gap:5px!important;width:150px!important;max-width:150px!important;min-width:0!important;height:39px!important;overflow:hidden!important;white-space:nowrap!important;text-overflow:ellipsis!important;font-size:.84rem!important;line-height:1.1!important}
    .bars .bar>div{grid-column:2!important;grid-row:1!important;position:relative!important;width:100%!important;min-width:0!important;height:24px!important;min-height:24px!important;margin:0!important;box-sizing:border-box!important}
    .bars .bar .bardelta{grid-column:2!important;grid-row:2!important;width:100%!important;height:12px!important;min-height:0!important;margin:0!important;padding:0!important;line-height:12px!important;font-size:.60rem!important;white-space:nowrap!important}
    .bars .bar>b .ranknum{flex:0 0 auto!important;min-width:27px!important;height:23px!important}

    /* Correção específica dos gráficos mostrados: nome curto e barra imediatamente ao lado. */
    #p-faixas .bars,
    #p-dia-faixa .bars,
    #p-companhia .bars,
    #p-motivacao .bars,
    #p-local .bars,
    #p-orcrim-vitima .bars,
    #p-orcrim-autores .bars,
    #p-bairro .bars{width:100%!important;max-width:100%!important}
    #p-faixas .bars .bar,
    #p-dia-faixa .bars .bar,
    #p-companhia .bars .bar,
    #p-motivacao .bars .bar,
    #p-local .bars .bar,
    #p-orcrim-vitima .bars .bar,
    #p-orcrim-autores .bars .bar,
    #p-bairro .bars .bar{grid-template-columns:150px minmax(0,1fr)!important;column-gap:4px!important}
    #p-faixas .bars .bar>b,
    #p-dia-faixa .bars .bar>b,
    #p-companhia .bars .bar>b,
    #p-motivacao .bars .bar>b,
    #p-local .bars .bar>b,
    #p-orcrim-vitima .bars .bar>b,
    #p-orcrim-autores .bars .bar>b,
    #p-bairro .bars .bar>b{width:150px!important;max-width:150px!important}

    @media(max-width:900px){
      .bars .bar{grid-template-columns:135px minmax(0,1fr)!important;column-gap:4px!important}
      .bars .bar>b{width:135px!important;max-width:135px!important}
    }
    @media(max-width:600px){
      .bars .bar{grid-template-columns:1fr!important;grid-template-rows:22px 22px 11px!important;gap:2px!important;padding:1px 0!important}
      .bars .bar>b{grid-column:1!important;grid-row:1!important;width:100%!important;height:22px!important;max-width:100%!important}
      .bars .bar>div{grid-column:1!important;grid-row:2!important;width:100%!important;height:22px!important;min-height:22px!important}
      .bars .bar .bardelta{grid-column:1!important;grid-row:3!important;width:100%!important;height:11px!important;line-height:11px!important;margin-left:27px!important}
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
