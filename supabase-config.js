window.SUPABASE_URL = 'https://rbpuatcdlbfqxfkbvgst.supabase.co';
window.SUPABASE_ANON_KEY = 'sb_publishable_AH0rCyKZ4J5SMfMwof3TkA_wkTXeg9D';
// Compatibilidade com versões antigas do dashboard: evita erro "p6 is not defined".
window.p6 = null;

// Melhoria visual dos gráficos horizontais já existentes no dashboard.
(function(){
  const css = `
  .bars{display:flex;flex-direction:column;gap:12px;padding:2px 0 4px}
  .bars .bar{display:grid;grid-template-columns:minmax(150px,34%) 1fr;gap:12px;align-items:center;padding:2px 0;transition:transform .15s ease}
  .bars .bar>b{font-size:.86rem;display:flex;align-items:center;gap:6px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bars .bar>b .ranknum{display:inline-flex;align-items:center;justify-content:center;min-width:27px;height:22px;border-radius:7px;background:var(--bg);color:var(--mut);font-size:.68rem;font-weight:800}
  .bars .bar>div{position:relative;height:25px;background:linear-gradient(90deg,var(--bg),color-mix(in srgb,var(--line) 65%,transparent));border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;align-items:center;min-width:0}
  .bars .bar>div i{display:block;height:100%;min-width:0;background:linear-gradient(90deg,var(--acc),var(--hi));border-radius:7px;transition:width .45s cubic-bezier(.2,.7,.2,1);box-shadow:0 1px 4px rgba(11,37,69,.16)}
  .bars .bar:first-child>div i{background:linear-gradient(90deg,var(--hi),#4f78a8)}
  .bars .bar>div em{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-style:normal;font-size:.72rem;font-weight:800;color:var(--ink);background:rgba(255,255,255,.84);padding:2px 6px;border-radius:6px;white-space:nowrap;backdrop-filter:blur(2px)}
  .bars .bar:hover{transform:translateX(2px)}
  .bars .bar:hover>div i{filter:brightness(1.08)}
  .bars .bar .bardelta{grid-column:2;margin:-7px 0 0;font-size:.65rem;font-weight:800}
  @media(max-width:700px){.bars .bar{grid-template-columns:1fr;gap:5px}.bars .bar .bardelta{grid-column:1;margin:-2px 0 0 32px}.bars .bar>div{height:22px}}
  `;
  const style=document.createElement('style');
  style.id='dashboard-chart-enhancements';
  style.textContent=css;
  (document.head||document.documentElement).appendChild(style);
})();
