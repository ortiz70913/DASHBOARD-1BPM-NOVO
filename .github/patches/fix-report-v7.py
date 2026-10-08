from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V2: usa o mesmo cliente Supabase autenticado do dashboard, com paginação.
start = s.find('async function getRows(){')
if start >= 0:
    end = s.find('function monthKey', start)
    if end >= 0:
        new = r'''async function getRows(){
      var out=[],from=0,page=1000;
      while(true){
        const {data,error}=await sb.from('ocorrencias').select('*').order('data',{ascending:true}).range(from,from+page-1);
        if(error) throw new Error('Erro na base: '+(error.message||error));
        (data||[]).forEach(function(x){out.push([x.data,x.cia||0,x.turno||0,x.bairro||'Não informado',x.dia_semana||'',x.hora==null?-1:x.hora,x.presos_ids||'',x.motivacao||'',x.arma||'Não informado',x.local_fato||'Não informado',x.abordagem||'Não informado',x.logradouro||'Não informado',x.tipo_veiculo||'Não informado',x.modelo||'Não informado',x.marca||'Não informado',x.bairro_recuperacao||'',x.estabelecimento||'',x.tipo_roubo||'',x.material||'',x.modo_acao||'',x.recuperacao||'',x.logradouro_recuperacao||'',x.tipo_local||'',x.empresa||'',x.linha||'',x.orcrim_vitima||'Não informado',x.orcrim_autor||'Não informado']);});
        if(!data||data.length<page) break;
        from += page;
      }
      return out.filter(function(x){return x&&x[0]});
    }
    '''
        s = s[:start] + new + s[end:]

# V5: mesma correção para a rotina auxiliar, caso ela seja a que estiver ativa no navegador.
start = s.find('async function fetchRows(){')
if start >= 0:
    end = s.find('function fallbackRows', start)
    if end >= 0:
        new = r'''async function fetchRows(){
    if(typeof sb==='undefined') throw new Error('Cliente Supabase não disponível.');
    var all=[],offset=0,size=1000;
    while(true){
      var res=await sb.from('ocorrencias').select('*').order('data',{ascending:true}).range(offset,offset+size-1);
      if(res.error) throw new Error(res.error.message||String(res.error));
      var a=res.data||[]; all=all.concat(a);
      if(a.length<size) break;
      offset+=size;
    }
    return all.map(rowFromDb).filter(function(r){return r.data;});
  }
  '''
        s = s[:start] + new + s[end:]

# V6: troca o fetch REST com anon key pelo cliente autenticado do dashboard.
start = s.find('async function load(){')
if start >= 0:
    end = s.find('function ui()', start)
    if end >= 0:
        new = r'''async function load(){
  if(typeof sb==='undefined') throw Error('Cliente Supabase não disponível');
  var out=[],off=0,page=1000;
  while(true){
    var res=await sb.from('ocorrencias').select('*').order('data',{ascending:true}).range(off,off+page-1);
    if(res.error) throw Error(res.error.message||String(res.error));
    var a=res.data||[]; out=out.concat(a);
    if(a.length<page) break;
    off+=page;
  }
  return out.map(db).filter(function(x){return x.data;});
}
'''
        s = s[:start] + new + s[end:]

marker='<!-- RELATORIO_INTELIGENCIA_V7_AUTH -->'
if marker not in s:
    s=s.replace('<body>', '<body>\n'+marker)

p.write_text(s,encoding='utf-8')
