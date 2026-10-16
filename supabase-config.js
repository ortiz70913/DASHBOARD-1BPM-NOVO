window.SUPABASE_URL = 'https://rbpuatcdlbfqxfkbvgst.supabase.co';
window.SUPABASE_ANON_KEY = 'sb_publishable_AH0rCyKZ4J5SMfMwof3TkA_wkTXeg9D';
window.p6 = null;

/* LAYOUT FINAL DOS GRAFICOS - compacto e proporcional */
(function(){
  const style=document.createElement('style');
  style.id='dashboard-chart-layout-final';
  style.textContent=`
    .bars{display:flex!important;flex-direction:column!important;width:100%!important;max-width:100%!important;gap:3px!important;padding:0!important;margin:0!important;box-sizing:border-box!important}
    .bars .bar{display:grid!important;grid-template-columns:minmax(170px,25%) minmax(0,1fr)!important;grid-template-rows:26px 12px!important;gap:1px 9px!important;width:100%!important;min-width:0!important;height:auto!important;min-height:0!important;padding:1px 0!important;margin:0!important;align-items:center!important;box-sizing:border-box!important}
    .bars .bar>b{grid-column:1!important;grid-row:1 / span 2!important;display:flex!important;align-items:center!important;gap:7px!important;width:100%!important;min-width:0!important;height:39px!important;overflow:hidden!important;white-space:nowrap!important;text-overflow:ellipsis!important;font-size:.84rem!important;line-height:1.1!important}
    .bars .bar>b .ranknum{display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;min-width:27px!important;height:23px!important;border-radius:7px!important;background:var(--bg)!important;color:var(--mut)!important;border:1px solid var(--line)!important;font-size:.67rem!important;font-weight:800!important}
    .bars .bar:nth-child(1)>b .ranknum{background:#0b2545!important;color:#fff!important;border-color:#0b2545!important}
    .bars .bar>div{grid-column:2!important;grid-row:1!important;position:relative!important;width:100%!important;min-width:0!important;height:24px!important;min-height:24px!important;margin:0!important;background:linear-gradient(90deg,var(--bg),rgba(223,229,236,.55))!important;border:1px solid var(--line)!important;border-radius:9px!important;overflow:hidden!important;display:flex!important;align-items:center!important;box-sizing:border-box!important}
    .bars .bar>div i{display:block!important;height:100%!important;min-width:3px!important;background:linear-gradient(90deg,var(--acc),var(--hi))!important;border-radius:8px!important;transition:width .35s ease!important}
    .bars .bar:first-child>div i{background:linear-gradient(90deg,var(--hi),#4f78a8)!important}
    .bars .bar>div em{position:absolute!important;right:7px!important;top:50%!important;transform:translateY(-50%)!important;font-style:normal!important;font-size:.68rem!important;font-weight:800!important;color:var(--ink)!important;background:rgba(255,255,255,.92)!important;padding:1px 6px!important;border-radius:6px!important;white-space:nowrap!important}
    .bars .bar .bardelta{grid-column:2!important;grid-row:2!important;width:100%!important;height:12px!important;min-height:0!important;margin:0!important;padding:0!important;line-height:12px!important;font-size:.60rem!important;font-weight:800!important;white-space:nowrap!important}

    #painelInt .pi-months{display:grid!important;grid-template-columns:repeat(10,minmax(0,1fr))!important;grid-template-rows:1fr!important;grid-auto-flow:column!important;width:100%!important;min-width:0!important;max-width:100%!important;height:190px!important;gap:clamp(4px,.7vw,9px)!important;padding:22px 8px 6px!important;margin:2px 0 0!important;align-items:stretch!important;overflow:hidden!important;box-sizing:border-box!important}
    #painelInt .pi-month{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-end!important;width:100%!important;min-width:0!important;height:100%!important;position:relative!important;box-sizing:border-box!important}
    #painelInt .pi-month::before{content:''!important;position:absolute!important;left:50%!important;top:0!important;bottom:27px!important;border-left:1px dashed color-mix(in srgb,var(--line) 70%,transparent)!important;transform:translateX(-50%)!important;pointer-events:none!important;opacity:.45!important}
    #painelInt .pi-bar{width:clamp(22px,65%,56px)!important;max-width:56px!important;min-height:4px!important;border-radius:8px 8px 3px 3px!important;background:linear-gradient(180deg,var(--hi),var(--acc))!important;position:relative!important;z-index:1!important}
    #painelInt .pi-bar b{position:absolute!important;top:-18px!important;left:50%!important;transform:translateX(-50%)!important;font-size:.68rem!important;font-weight:900!important;color:var(--ink)!important;white-space:nowrap!important}
    #painelInt .pi-month small{position:relative!important;z-index:2!important;margin-top:4px!important;color:var(--mut)!important;font-size:.65rem!important;font-weight:800!important;white-space:nowrap!important}

    #p-mes #mes,#p-mes #mes.monthly-chart-fixed{display:block!important;width:100%!important;min-width:0!important;max-width:100%!important;margin:0!important;padding:0 4px 3px!important;overflow:hidden!important;box-sizing:border-box!important}
    #p-mes #mes>.cols,#p-mes #mes.monthly-chart-fixed>.cols{display:grid!important;grid-template-columns:repeat(10,minmax(0,1fr))!important;grid-template-rows:1fr!important;width:100%!important;min-width:0!important;max-width:100%!important;height:165px!important;gap:clamp(4px,.7vw,9px)!important;padding:18px 0 0!important;margin:0!important;align-items:end!important;box-sizing:border-box!important}
    #p-mes #mes>.cols>.col,#p-mes #mes.monthly-chart-fixed>.cols>.col{display:flex!important;flex-direction:column!important;justify-content:flex-end!important;align-items:center!important;width:100%!important;min-width:0!important;height:100%!important;position:relative!important;box-sizing:border-box!important}
    #p-mes #mes>.cols>.col i,#p-mes #mes.monthly-chart-fixed>.cols>.col i{display:block!important;width:clamp(16px,52%,56px)!important;max-width:56px!important;min-width:12px!important}
    #p-mes #mes>.cols>.col em,#p-mes #mes.monthly-chart-fixed>.cols>.col em{margin-bottom:3px!important;font-size:.70rem!important}
    #p-mes #mes.monthly-chart-fixed>.cols>.col .month-label{display:block!important;width:100%!important;height:17px!important;line-height:17px!important;margin-top:3px!important;text-align:center!important;font-size:.68rem!important;font-weight:800!important;color:var(--mut)!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
    #p-mes #mes>.lab{display:grid!important;grid-template-columns:repeat(10,minmax(0,1fr))!important;width:100%!important;min-width:0!important;gap:clamp(4px,.7vw,9px)!important;margin:3px 0 0!important;padding:0!important}
    #p-mes #mes>.lab>span{display:block!important;width:100%!important;min-width:0!important;text-align:center!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;font-size:.68rem!important}
    #p-mes #mes .coldelta{display:block!important;min-height:10px!important;font-size:.56rem!important;white-space:nowrap!important}

    @media(max-width:900px){
      .bars .bar{grid-template-columns:minmax(130px,28%) minmax(0,1fr)!important}
      #painelInt .pi-months{height:175px!important;padding-top:20px!important}
      #p-mes #mes>.cols,#p-mes #mes.monthly-chart-fixed>.cols{height:155px!important;padding-top:18px!important}
    }
    @media(max-width:600px){
      .bars{gap:4px!important}
      .bars .bar{grid-template-columns:1fr!important;grid-template-rows:22px 22px 11px!important;gap:2px!important;padding:1px 0!important}
      .bars .bar>b{grid-column:1!important;grid-row:1!important;height:22px!important}
      .bars .bar>div{grid-column:1!important;grid-row:2!important;height:22px!important;min-height:22px!important}
      .bars .bar .bardelta{grid-column:1!important;grid-row:3!important;height:11px!important;line-height:11px!important;margin-left:27px!important}
      #painelInt .pi-months{height:165px!important;padding-top:20px!important;gap:3px!important}
      #p-mes #mes>.cols,#p-mes #mes.monthly-chart-fixed>.cols{height:150px!important;gap:3px!important}
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
