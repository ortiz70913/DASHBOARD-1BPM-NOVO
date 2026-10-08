from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
new="""    async function getRows(){
      var out=[],url=window['SUPABASE_URL'],key=window['SUPABASE_'+'ANON_KEY'];
      if(!url||!key) throw new Error('Configuração da base não encontrada');
      var r=await fetch(url+'/rest/v1/ocorrencias?select=*&order=data.asc',{headers:{apikey:key,Authorization:'Bearer '+key}});
      if(!r.ok) throw new Error('Erro na base: HTTP '+r.status);
      var a=await r.json();
      a.forEach(function(x){out.push([x.data,x.cia||0,x.turno||0,x.bairro||'Não informado',x.dia_semana||'',x.hora==null?-1:x.hora,x.presos_ids||'',x.motivacao||'',x.arma||'Não informado',x.local_fato||'Não informado',x.abordagem||'Não informado',x.logradouro||'Não informado',x.tipo_veiculo||'Não informado',x.modelo||'Não informado',x.marca||'Não informado',x.bairro_recuperacao||'',x.estabelecimento||'',x.tipo_roubo||'',x.material||'',x.modo_acao||'',x.recuperacao||'',x.logradouro_recuperacao||'',x.tipo_local||'',x.empresa||'',x.linha||'',x.orcrim_vitima||'Não informado',x.orcrim_autor||'Não informado']);});
      return out.filter(function(x){return x&&x[0]});
    }"""
pat=r'    async function getRows\(\)\{.*?\n    \}\n\n    function monthKey'
s,n=re.subn(pat,new+'\n\n    function monthKey',s,count=1,flags=re.S)
if n!=1: raise SystemExit('getRows não encontrado')
p.write_text(s,encoding='utf-8')
