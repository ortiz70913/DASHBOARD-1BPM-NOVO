from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_get = '''    function getRows(){\n      try{\n        var out=[];\n        if(typeof DS!=='undefined' && DS){\n          Object.keys(DS).forEach(function(k){\n            var arr=DS[k] && Array.isArray(DS[k].R) ? DS[k].R : [];\n            out=out.concat(arr);\n          });\n        }\n        return out.filter(function(r){return r && r[0] && r[0]!=='';});\n      }catch(e){ return []; }\n    }'''

new_get = '''    async function getRows(){\n      var out=[];\n      var fallback=[];\n      try{\n        if(typeof DS!=='undefined' && DS){\n          Object.keys(DS).forEach(function(k){\n            var arr=DS[k] && Array.isArray(DS[k].R) ? DS[k].R : [];\n            fallback=fallback.concat(arr);\n          });\n        }\n      }catch(e){}\n\n      try{\n        if(typeof sb!=='undefined' && sb && typeof DS!=='undefined' && DS){\n          var keys=Object.keys(DS);\n          for(var ki=0;ki<keys.length;ki++){\n            var k=keys[ki], from=0, page=1000;\n            while(true){\n              var resp=await sb.from('ocorrencias').select('*').eq('aba',k).order('data',{ascending:true}).range(from,from+page-1);\n              if(resp.error) throw resp.error;\n              var data=resp.data||[];\n              out=out.concat(data.map(dbToRow));\n              if(data.length<page) break;\n              from+=page;\n            }\n          }\n        }\n      }catch(e){\n        console.warn('Relatório de Inteligência: consulta direta falhou; usando dados do dashboard.',e);\n      }\n\n      if(!out.length) out=fallback;\n      return out.filter(function(r){return r && r[0] && r[0]!=='';});\n    }'''

if old_get not in s:
    raise SystemExit('Bloco getRows não encontrado')
s = s.replace(old_get, new_get, 1)

old_render = '''    function render(){\n      var all=getRows(), cia=document.getElementById('riCia').value, mes=document.getElementById('riMes').value;'''
new_render = '''    async function render(){\n      var all=await getRows(), cia=document.getElementById('riCia').value, mes=document.getElementById('riMes').value;'''
if old_render not in s:
    raise SystemExit('Bloco render não encontrado')
s = s.replace(old_render, new_render, 1)

# Show an explicit loading state when opening/updating the report.
old_open = '''    function openReport(){\n      panel.hidden=false;\n      btn.setAttribute('aria-pressed','true');\n      render();\n    }'''
new_open = '''    function openReport(){\n      panel.hidden=false;\n      btn.setAttribute('aria-pressed','true');\n      document.getElementById('riResumo').innerHTML='<div class="ri-card"><b>...</b><span>Carregando dados do Supabase</span></div>';\n      document.getElementById('riConteudo').innerHTML='<div class="ri-box"><div class="ri-empty">Consultando a base de ocorrências...</div></div>';\n      render();\n    }'''
if old_open not in s:
    raise SystemExit('Bloco openReport não encontrado')
s = s.replace(old_open, new_open, 1)

p.write_text(s, encoding='utf-8')
print('Patch aplicado: Relatório de Inteligência consulta Supabase diretamente.')
