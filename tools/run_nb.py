"""Convierte un .py con celdas '# %%' en .ipynb y lo ejecuta en un solo espacio de nombres, guardando salidas."""
import sys, json, io, base64, contextlib, traceback, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
src, dst = sys.argv[1], sys.argv[2]
txt = open(src, encoding='utf-8').read()
cells = []; cur = None
for line in txt.splitlines():
    if line.startswith('# %% [markdown]'):
        cur = {'type':'markdown','lines':[]}; cells.append(cur); continue
    if line.startswith('# %%'):
        cur = {'type':'code','lines':[]}; cells.append(cur); continue
    if cur is None: continue
    cur['lines'].append(line)
ns = {'__name__':'__main__'}
nb = {'cells':[], 'metadata':{'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},
      'language_info':{'name':'python','version':sys.version.split()[0]}}, 'nbformat':4, 'nbformat_minor':5}
n = 0
for i,c in enumerate(cells):
    lines = c['lines']
    while lines and not lines[-1].strip(): lines.pop()
    while lines and not lines[0].strip(): lines.pop(0)
    if c['type']=='markdown':
        md = [l[2:] if l.startswith('# ') else (l[1:] if l.startswith('#') else l) for l in lines]
        nb['cells'].append({'cell_type':'markdown','id':f'c{i}','metadata':{},'source':'\n'.join(md)})
        continue
    n += 1; code = '\n'.join(lines); outs = []
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, f'<celda {n}>', 'exec'), ns)
    except Exception:
        print(buf.getvalue()); traceback.print_exc(); print('FALLÓ CELDA', n); sys.exit(1)
    if buf.getvalue():
        outs.append({'output_type':'stream','name':'stdout','text':buf.getvalue()})
    for fnum in plt.get_fignums():
        fig = plt.figure(fnum); b = io.BytesIO(); fig.savefig(b, format='png', dpi=110, bbox_inches='tight')
        outs.append({'output_type':'display_data','metadata':{},'data':{'image/png':base64.b64encode(b.getvalue()).decode(),'text/plain':'<Figure>'}})
    plt.close('all')
    nb['cells'].append({'cell_type':'code','id':f'c{i}','metadata':{},'execution_count':n,'source':code,'outputs':outs})
    print(f'celda {n} ok', file=sys.stderr)
json.dump(nb, open(dst,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('cuaderno escrito', dst)
