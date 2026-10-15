window.SUPABASE_URL = 'https://rbpuatcdlbfqxfkbvgst.supabase.co';
window.SUPABASE_ANON_KEY = 'sb_publishable_AH0rCyKZ4J5SMfMwof3TkA_wkTXeg9D';
// Compatibilidade com versões antigas do dashboard: evita erro "p6 is not defined".
window.p6 = null;

// Melhorias visuais dos gráficos do dashboard.
(function(){
  const css = `
  .bars{display:flex!important;flex-direction:column!important;gap:10px!important;padding:4px 0 6px!important;width:100%!important}
  .bars .bar{display:grid!important;grid-template-columns:minmax(145px,32%) minmax(0,1fr)!important;grid-template-rows:auto auto!important;gap:4px 12px!important;align-items:center!important;padding:5px 0!important;min-height:48px!important;transition:transform .15s ease,filter .15s ease!important}
  .bars .bar>b{grid-column:1!important;grid-row:1 / span 2!important;font-size:.86rem!important;display:flex!important;align-items:center!important;gap:7px!important;min-width:0!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
  .bars .bar>b .ranknum{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-width:29px!important;height:24px!important;border-radius:7px!important;background:var(--bg)!important;color:var(--mut)!important;border:1px solid var(--line)!important;font-size:.68rem!important;font-weight:800!important;flex:0 0 auto!important}
  .bars .bar>div{grid-column:2!important;grid-row:1!important;position:relative!important;height:25px!important;background:linear-gradient(90deg,var(--bg),rgba(223,229,236,.55))!important;border:1px solid var(--line)!important;border-radius:9px!important;overflow:hidden!important;display:flex!important;align-items:center!important;min-width:0!important;width:100%!important}
  .bars .bar>div i{display:block!important;height:100%!important;min-width:3px!important;background:linear-gradient(90deg,var(--acc),var(--hi))!important;border-radius:8px!important;transition:width .45s cubic-bezier(.2,.7,.2,1)!important;box-shadow:0 1px 5px rgba(11,37,69,.18)!important}
  .bars .bar:first-child>div i{background:linear-gradient(90deg,var(--hi),#4f78a8)!important}
  .bars .bar>div em{position:absolute!important;right:7px!important;top:50%!important;transform:translateY(-50%)!important;font-style:normal!important;font-size:.72rem!important;font-weight:800!important;color:var(--ink)!important;background:rgba(255,255,255,.9)!important;padding:2px 7px!important;border-radius:6px!important;white-space:nowrap!important;backdrop-filter:blur(2px)!important}
  .bars .bar .bardelta{grid-column:2!important;grid-row:2!important;margin:0!important;font-size:.65rem!important;font-weight:800!important}
  .bars .bar:hover{transform:translateX(3px)!important;filter:brightness(1.02)!important}
  .bars .bar:hover>div i{filter:brightness(1.1)!important}
  .bars .bar:nth-child(1)>b .ranknum{background:#0b2545!important;color:#fff!important;border-color:#0b2545!important}

  #painelInt .pi-months{display:grid!important;grid-template-columns:repeat(9,minmax(110px,1fr))!important;grid-template-rows:1fr!important;grid-auto-flow:column!important;gap:18px!important;align-items:stretch!important;height:250px!important;padding:30px 18px 10px!important;margin-top:8px!important;border-bottom:1px solid var(--line)!important;overflow-x:auto!important;overflow-y:visible!important;box-sizing:border-box!important}
  #painelInt .pi-month{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-end!important;height:100%!important;min-width:110px!important;position:relative!important}
  #painelInt .pi-month::before{content:''!important;position:absolute!important;left:50%!important;top:0!important;bottom:30px!important;border-left:1px dashed color-mix(in srgb,var(--line) 75%,transparent)!important;transform:translateX(-50%)!important;pointer-events:none!important;opacity:.55!important}
  #painelInt .pi-bar{width:min(72px,70%)!important;min-height:5px!important;border-radius:8px 8px 3px 3px!important;background:linear-gradient(180deg,var(--hi),var(--acc))!important;position:relative!important;z-index:1!important;box-shadow:0 3px 8px rgba(11,37,69,.16)!important;transition:height .45s cubic-bezier(.2,.7,.2,1),filter .15s ease!important}
  #painelInt .pi-bar:hover{filter:brightness(1.08)!important}
  #painelInt .pi-bar b{position:absolute!important;top:-24px!important;left:50%!important;transform:translateX(-50%)!important;font-size:.78rem!important;font-weight:900!important;color:var(--ink)!important;white-space:nowrap!important}
  #painelInt .pi-month small{position:relative!important;z-index:2!important;margin-top:9px!important;color:var(--mut)!important;font-size:.7rem!important;font-weight:800!important;white-space:nowrap!important}

  #p-mes #mes{display:block!important;width:100%!important;min-width:0!important;margin:0!important;padding:0 12px 8px!important;overflow-x:auto!important;overflow-y:visible!important}
  #p-mes #mes>.cols{display:grid!important;grid-template-columns:repeat(9,minmax(0,1fr))!important;grid-template-rows:1fr!important;width:100%!important;min-width:900px!important;height:165px!important;align-items:end!important;gap:14px!important;padding:0!important;margin:0!important;box-sizing:border-box!important}
  #p-mes #mes>.cols>.col{display:flex!important;flex-direction:column!important;justify-content:flex-end!important;align-items:center!important;min-width:0!important;width:auto!important;max-width:none!important;flex:initial!important;position:relative!important;height:100%!important}
  #p-mes #mes>.cols>.col i{width:58%!important;max-width:62px!important;min-width:20px!important;display:block!important;flex:0 0 auto!important;border-radius:8px 8px 2px 2px!important}
  #p-mes #mes>.cols>.col em{margin-bottom:5px!important;position:relative!important;z-index:2!important}
  #p-mes #mes>.lab{display:grid!important;grid-template-columns:repeat(9,minmax(0,1fr))!important;width:100%!important;min-width:900px!important;gap:14px!important;margin:7px 0 0!important;padding:0!important;box-sizing:border-box!important}
  #p-mes #mes>.lab>span{display:block!important;width:auto!important;min-width:0!important;text-align:center!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;font-size:.7rem!important}
  #p-mes #mes .coldelta{display:block!important;white-space:nowrap!important;min-height:11px!important;font-size:.58rem!important}

  @media(max-width:1100px){
    #painelInt .pi-months{grid-template-columns:repeat(9,minmax(120px,1fr))!important;gap:16px!important;overflow-x:auto!important}
    #p-mes #mes>.cols,#p-mes #mes>.lab{min-width:900px!important}
  }
  @media(max-width:700px){
    .bars .bar{grid-template-columns:1fr!important;grid-template-rows:auto auto auto!important;gap:5px!important}
    .bars .bar>b{grid-column:1!important;grid-row:1!important}
    .bars .bar>div{grid-column:1!important;grid-row:2!important;height:23px!important}
    .bars .bar .bardelta{grid-column:1!important;grid-row:3!important;margin-left:34px!important}
    #painelInt .pi-months{grid-template-columns:repeat(9,120px)!important;grid-template-rows:1fr!important;gap:16px!important;height:230px!important;min-height:230px!important;padding:28px 12px 10px!important;overflow-x:auto!important}
    #painelInt .pi-month{height:190px!important;min-width:120px!important}
    #p-mes #mes{padding:0 8px 8px!important}
    #p-mes #mes>.cols,#p-mes #mes>.lab{min-width:900px!important;grid-template-columns:repeat(9,minmax(0,1fr))!important;gap:14px!important}
  }
  `;
  const style=document.createElement('style');
  style.id='dashboard-chart-enhancements-v7';
  style.textContent=css;
  (document.head||document.documentElement).appendChild(style);
})();

// Correção definitiva: cada mês passa a ficar dentro da própria coluna da barra.
// Isso elimina qualquer desalinhamento causado por estruturas independentes de .cols e .lab.
(function(){
  function fixMonthlyChart(){
    const root=document.getElementById('mes');
    if(!root)return;
    const cols=root.querySelector(':scope > .cols');
    const lab=root.querySelector(':scope > .lab');
    if(!cols || !lab)return;
    const labels=[...lab.children].map(x=>x.textContent.trim());
    const items=[...cols.children];
    if(!items.length || !labels.length)return;
    items.forEach((col,i)=>{
      let tag=col.querySelector('.month-label');
      if(!tag){tag=document.createElement('span');tag.className='month-label';col.appendChild(tag)}
      tag.textContent=labels[i]||'';
    });
    lab.remove();
    root.classList.add('monthly-chart-fixed');
  }
  const style=document.createElement('style');
  style.textContent=`
    #p-mes #mes.monthly-chart-fixed{overflow-x:auto!important;padding:0 12px 10px!important}
    #p-mes #mes.monthly-chart-fixed>.cols{display:grid!important;grid-template-columns:repeat(9,minmax(90px,1fr))!important;grid-template-rows:1fr!important;gap:14px!important;width:100%!important;min-width:900px!important;height:195px!important;align-items:end!important;margin:0!important;padding:0!important}
    #p-mes #mes.monthly-chart-fixed>.cols>.col{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-end!important;width:auto!important;min-width:0!important;height:100%!important;position:relative!important}
    #p-mes #mes.monthly-chart-fixed>.cols>.col .month-label{display:block!important;margin-top:8px!important;height:20px!important;line-height:20px!important;text-align:center!important;font-size:.72rem!important;font-weight:800!important;color:var(--mut)!important;white-space:nowrap!important}
    #p-mes #mes.monthly-chart-fixed>.cols>.col i{width:58%!important;max-width:62px!important;min-width:20px!important}
    #p-mes #mes.monthly-chart-fixed>.cols>.col em{margin-bottom:5px!important}
    @media(max-width:700px){#p-mes #mes.monthly-chart-fixed>.cols{min-width:900px!important;grid-template-columns:repeat(9,minmax(90px,1fr))!important}}
  `;
  document.head.appendChild(style);
  const run=()=>fixMonthlyChart();
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else setTimeout(run,0);
  const mo=new MutationObserver(()=>fixMonthlyChart());
  mo.observe(document.documentElement,{childList:true,subtree:true});
})();
