from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")
marker = "RELATORIO_INTELIGENCIA_PATCH_V2"
if marker in s:
    raise SystemExit(0)

injected = r'''
/* RELATORIO_INTELIGENCIA_PATCH_V2 */
(function(){
  function installRelatorioInteligencia(){
    if(document.getElementById('relatorioInteligenciaTab')) return;

    var host = document.getElementById('dsb') || document.querySelector('header') || document.body;
    var btn = document.createElement('button');
    btn.id = 'relatorioInteligenciaTab';
    btn.type = 'button';
    btn.textContent = '📋 Relatório de Inteligência';
    btn.setAttribute('aria-pressed','false');
    btn.style.cssText = 'margin:6px 4px;padding:9px 12px;border:1px solid var(--line,#dfe5ec);border-radius:9px;background:var(--card,#fff);color:var(--ink,#0f1c2e);font-weight:700;cursor:pointer;';
    host.appendChild(btn);

    var panel = document.createElement('section');
    panel.id = 'relatorioInteligenciaPanel';
    panel.hidden = true;
    panel.innerHTML = `
      <div class="ri-head">
        <div>
          <h2>📋 Relatório de Inteligência</h2>
          <div class="ri-sub">Dados carregados do banco utilizado pelo painel.</div>
        </div>
        <button type="button" id="riClose">Fechar</button>
      </div>
      <div class="ri-filters">
        <label>CIA
          <select id="riCia">
            <option value="">Todas</option>
            <option value="1">1ª CIA</option>
            <option value="2">2ª CIA</option>
            <option value="3">3ª CIA</option>
          </select>
        </label>
        <label>Mês
          <select id="riMes"><option value="">Todos</option></select>
        </label>
        <label>Pesquisar
          <input id="riBusca" type="search" placeholder="bairro, local, motivação, arma..." />
        </label>
        <button type="button" id="riAtualizar">↻ Atualizar</button>
      </div>
      <div id="riResumo" class="ri-cards"></div>
      <div id="riConteudo"></div>
    `;
    document.body.appendChild(panel);

    var css = document.createElement('style');
    css.textContent = `
      #relatorioInteligenciaPanel{position:fixed;inset:0;z-index:99999;background:var(--bg,#f4f6f9);color:var(--ink,#0f1c2e);overflow:auto;padding:18px}
      #relatorioInteligenciaPanel .ri-head{display:flex;justify-content:space-between;gap:16px;align-items:center;max-width:1500px;margin:0 auto 14px}
      #relatorioInteligenciaPanel h2{margin:0;font-size:22px}
      #relatorioInteligenciaPanel .ri-sub{color:var(--mut,#5b6b7f);font-size:13px}
      #relatorioInteligenciaPanel button,#relatorioInteligenciaPanel select,#relatorioInteligenciaPanel input{font:inherit}
      #relatorioInteligenciaPanel button{border:1px solid var(--line,#dfe5ec);border-radius:8px;padding:8px 11px;background:var(--card,#fff);color:inherit;cursor:pointer;font-weight:700}
      #relatorioInteligenciaPanel .ri-filters{max-width:1500px;margin:0 auto 14px;display:flex;flex-wrap:wrap;gap:10px;align-items:end}
      #relatorioInteligenciaPanel label{display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:700}
      #relatorioInteligenciaPanel select,#relatorioInteligenciaPanel input{min-width:150px;padding:9px;border:1px solid var(--line,#dfe5ec);border-radius:8px;background:var(--card,#fff);color:inherit}
      #relatorioInteligenciaPanel .ri-cards{max-width:1500px;margin:0 auto 14px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
      #relatorioInteligenciaPanel .ri-card{background:var(--card,#fff);border:1px solid var(--line,#dfe5ec);border-radius:10px;padding:12px}
      #relatorioInteligenciaPanel .ri-card b{display:block;font-size:21px}
      #relatorioInteligenciaPanel .ri-card span{font-size:12px;color:var(--mut,#5b6b7f)}
      #relatorioInteligenciaPanel .ri-box{max-width:1500px;margin:0 auto 14px;background:var(--card,#fff);border:1px solid var(--line,#dfe5ec);border-radius:10px;overflow:hidden}
      #relatorioInteligenciaPanel .ri-box h3{margin:0;padding:12px 14px;border-bottom:1px solid var(--line,#dfe5ec);font-size:15px}
      #relatorioInteligenciaPanel .ri-table-wrap{overflow:auto}
      #relatorioInteligenciaPanel table{width:100%;border-collapse:collapse;font-size:12px}
      #relatorioInteligenciaPanel th,#relatorioInteligenciaPanel td{padding:8px;border-bottom:1px solid var(--line,#dfe5ec);text-align:left;vertical-align:top;white-space:nowrap}
      #relatorioInteligenciaPanel th{position:sticky;top:0;background:var(--hd,#0b2545);color:var(--hdink,#fff)}
      #relatorioInteligenciaPanel .ri-empty{padding:24px;text-align:center;color:var(--mut,#5b6b7f)}
      @media(max-width:700px){#relatorioInteligenciaPanel{padding:10px}#relatorioInteligenciaPanel .ri-head{align-items:flex-start}.ri-filters label{width:100%}.ri-filters select,.ri-filters input{width:100%}}
    `;
    document.head.appendChild(css);

    function getRows(){
      try{
        var out=[];
        if(typeof DS!=='undefined' && DS){
          Object.keys(DS).forEach(function(k){
            var arr=DS[k] && Array.isArray(DS[k].R) ? DS[k].R : [];
            out=out.concat(arr);
          });
        }
        return out.filter(function(r){return r && r[0] && r[0]!=='';});
      }catch(e){ return []; }
    }

    function monthKey(v){
      var s=String(v||'');
      if(/^\d{4}-\d{2}/.test(s)) return s.slice(0,7);
      var m=s.match(/^(\d{2})\/(\d{2})\/(\d{4})/);
      return m ? m[3]+'-'+m[2] : '';
    }
    function dateLabel(v){
      var s=String(v||'');
      var m=s.match(/^(\d{4})-(\d{2})-(\d{2})/);
      if(m) return m[3]+'/'+m[2]+'/'+m[1];
      return s;
    }
    function esc(v){
      return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});
    }
    function ciaLabel(v){return v==1?'1ª CIA':v==2?'2ª CIA':v==3?'3ª CIA':String(v||'—');}
    function val(r,i){return r[i]==null||r[i]===''?'—':r[i];}

    function rebuildMonths(rows){
      var sel=document.getElementById('riMes'), current=sel.value;
      var months={};
      rows.forEach(function(r){var m=monthKey(r[0]);if(m)months[m]=1;});
      var keys=Object.keys(months).sort().reverse();
      sel.innerHTML='<option value="">Todos</option>'+keys.map(function(m){
        var parts=m.split('-'); return '<option value="'+m+'">'+parts[1]+'/'+parts[0]+'</option>';
      }).join('');
      if(keys.indexOf(current)>=0) sel.value=current;
    }

    function render(){
      var all=getRows(), cia=document.getElementById('riCia').value, mes=document.getElementById('riMes').value;
      var q=document.getElementById('riBusca').value.trim().toLowerCase();
      rebuildMonths(all);
      var rows=all.filter(function(r){
        if(cia && String(r[1])!==cia) return false;
        if(mes && monthKey(r[0])!==mes) return false;
        if(q){
          var text=[r[0],r[1],r[2],r[3],r[4],r[5],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[16],r[17],r[18],r[19],r[20],r[22],r[23],r[24],r[25],r[26]].join(' ').toLowerCase();
          if(text.indexOf(q)<0) return false;
        }
        return true;
      });
      rows.sort(function(a,b){return String(b[0]).localeCompare(String(a[0])) || Number(b[5]||0)-Number(a[5]||0);});

      var bairros={},armas={},dias={};
      rows.forEach(function(r){
        var b=String(r[3]||'Não informado'); bairros[b]=(bairros[b]||0)+1;
        var a=String(r[8]||'Não informado'); armas[a]=(armas[a]||0)+1;
        dias[monthKey(r[0])+'|'+String(r[0])]=1;
      });
      function top(obj,n){return Object.keys(obj).sort(function(a,b){return obj[b]-obj[a];}).slice(0,n).map(function(k){return esc(k)+' ('+obj[k]+')';}).join(', ')||'—';}

      document.getElementById('riResumo').innerHTML=[
        ['Ocorrências',rows.length],
        ['Dias com registros',Object.keys(dias).length],
        ['Bairros',Object.keys(bairros).length],
        ['Principal bairro',top(bairros,1)],
        ['Armas mais registradas',top(armas,3)]
      ].map(function(x){return '<div class="ri-card"><b>'+esc(x[1])+'</b><span>'+x[0]+'</span></div>';}).join('');

      if(!rows.length){
        document.getElementById('riConteudo').innerHTML='<div class="ri-box"><div class="ri-empty">Nenhum dado encontrado para os filtros selecionados.</div></div>';
        return;
      }

      var head=['Data','CIA','Turno','Bairro','Dia','Hora','Presos','Motivação','Arma','Local do fato','Abordagem','Logradouro','Veículo','Modelo','Marca','Estabelecimento','Tipo de roubo','Material','Modo de ação','Recuperação','Tipo de local','Empresa','Linha','ORCRIM vítima','ORCRIM autor'];
      var html='<div class="ri-box"><h3>Detalhamento — '+rows.length+' registro(s)</h3><div class="ri-table-wrap"><table><thead><tr>'+head.map(function(h){return '<th>'+h+'</th>';}).join('')+'</tr></thead><tbody>';
      rows.forEach(function(r){
        html+='<tr>'+ '<td>'+esc(dateLabel(r[0]))+'</td><td>'+esc(ciaLabel(r[1]))+'</td><td>'+esc(val(r,2))+'</td><td>'+esc(val(r,3))+'</td><td>'+esc(val(r,4))+'</td><td>'+esc(val(r,5))+'</td><td>'+esc(val(r,6))+'</td><td>'+esc(val(r,7))+'</td><td>'+esc(val(r,8))+'</td><td>'+esc(val(r,9))+'</td><td>'+esc(val(r,10))+'</td><td>'+esc(val(r,11))+'</td><td>'+esc(val(r,12))+'</td><td>'+esc(val(r,13))+'</td><td>'+esc(val(r,14))+'</td><td>'+esc(val(r,16))+'</td><td>'+esc(val(r,17))+'</td><td>'+esc(val(r,18))+'</td><td>'+esc(val(r,19))+'</td><td>'+esc(val(r,20))+'</td><td>'+esc(val(r,22))+'</td><td>'+esc(val(r,23))+'</td><td>'+esc(val(r,24))+'</td><td>'+esc(val(r,25))+'</td><td>'+esc(val(r,26))+'</td>'+ '</tr>';
      });
      html+='</tbody></table></div></div>';
      document.getElementById('riConteudo').innerHTML=html;
    }

    function openReport(){
      panel.hidden=false;
      btn.setAttribute('aria-pressed','true');
      render();
    }
    function closeReport(){
      panel.hidden=true;
      btn.setAttribute('aria-pressed','false');
    }

    btn.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();openReport();});
    document.getElementById('riClose').addEventListener('click',closeReport);
    document.getElementById('riAtualizar').addEventListener('click',render);
    ['riCia','riMes','riBusca'].forEach(function(id){
      document.getElementById(id).addEventListener('input',render);
      document.getElementById(id).addEventListener('change',render);
    });
    document.addEventListener('keydown',function(e){if(e.key==='Escape' && !panel.hidden)closeReport();});
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',installRelatorioInteligencia);
  else installRelatorioInteligencia();
})();
'''
needle = "</script>"
pos = s.rfind(needle)
if pos < 0:
    raise SystemExit("Nao foi encontrado o fechamento </script> no index.html")
s = s[:pos] + injected + "\n" + s[pos:]
p.write_text(s, encoding="utf-8")
print("patch applied")
