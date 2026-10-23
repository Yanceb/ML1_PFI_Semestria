"""Unifica las 8 programaciones académicas (pregrado presencial, Universidad EAN) en una tabla larga."""
import re, unicodedata, glob, os
import pandas as pd, numpy as np

PERIODOS = {
 'PROGRAMACION_PREGRADO_PRESENCIAL_2022-2_C4_V1.xlsx':'2022-2',
 'PROGRAMACIoN_PREGRADO-PRESENCIAL_2023-C2-18042023.xlsx':'2023-1',
 'Pregrado-presencial_Planta-fisica-2023-2.xlsx':'2023-2',
 'ProgramacionWebPregradoPresencial2024-1V6.xlsx':'2024-1',
 'Programacion_Web_Pregrado_Presencial_2024-2_5.xlsx':'2024-2',
 'Web_Pregrado_Presencial_2025-1_S1-C1 (1).xlsx':'2025-1',
 'Pregrado_Presencial_2025-2-v1 (2).xlsx':'2025-2',
 '2026-1_V7_31012026_PREGRADO_PRESENCIAL.xlsx':'2026-1',
}
FACULTADES = ['FIN','FAFCE','FHCS']

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().upper()
    return re.sub(r'\s+',' ', s).strip()

DIAS = {'LUN':['LUNES','LUN','L'], 'MAR':['MARTES','MAR','M'], 'MIE':['MIERCOLES','MIE','MI'],
        'JUE':['JUEVES','JUE','J'], 'VIE':['VIERNES','VIE','V'], 'SAB':['SABADO','SAB','S']}

def a_hora(v):
    if pd.isna(v): return np.nan
    if hasattr(v,'hour'): return v.hour + v.minute/60
    m = re.match(r'(\d{1,2}):(\d{2})', str(v))
    if m: return int(m.group(1)) + int(m.group(2))/60
    try:
        f = float(v);  return f*24 if f < 1 else np.nan
    except: return np.nan

def leer_hoja(ruta, hoja, periodo):
    raw = pd.read_excel(ruta, sheet_name=hoja, header=None)
    hdr = None
    for i in range(25):
        fila = [norm(x) for x in raw.iloc[i].tolist()]
        if any('HORA' in x and 'INICIO' in x for x in fila): hdr = i; break
    if hdr is None: return None
    cols = [norm(x) for x in raw.iloc[hdr].tolist()]
    df = raw.iloc[hdr+1:].copy(); df.columns = range(len(cols))
    def buscar(pred):
        for j,c in enumerate(cols):
            if pred(c): return j
        return None
    j_nom = buscar(lambda c: ('DENOMINACION' in c and 'UNIDAD' in c) or c.startswith('NOMBRE UNIDAD') or c=='UNIDAD DE ESTUDIO')
    if j_nom is None: j_nom = buscar(lambda c: c.startswith('DENOMINACION GRUPO'))
    j_cod = buscar(lambda c: c in ('CODIGO UE','CODIGO UNIDAD DE ESTUDIO','CODIGO'))
    j_grp = buscar(lambda c: c in ('CODIGO DEL GRUPO','PAQUETE DE EVENTOS'))
    j_hi = buscar(lambda c: 'HORA' in c and 'INICIO' in c)
    j_hf = buscar(lambda c: 'HORA' in c and ('FIN' in c))
    j_cre = buscar(lambda c: 'CREDITOS' in c)
    j_tip = buscar(lambda c: c.startswith('TIPO DE UNIDAD') or c=='TIPOLOGIA' or (c=='TIPO DE OFERTA' and periodo=='2026-1'))
    j_cic = buscar(lambda c: c=='CICLO' or c.startswith('CICLO -'))
    j_fi = buscar(lambda c: c.startswith('FECHA INICIO'))
    j_ff = buscar(lambda c: c.startswith('FECHA FIN'))
    j_prof = buscar(lambda c: c.startswith('DOCENTE') or c.startswith('PROFESOR'))
    jd = {}
    for d, alias in DIAS.items():
        jd[d] = buscar(lambda c, a=alias: c in a)
    out = pd.DataFrame({
        'periodo': periodo, 'facultad': hoja,
        'nombre_grupo': df[j_nom] if j_nom is not None else np.nan,
        'codigo_raw': df[j_cod] if j_cod is not None else (df[j_grp] if j_grp is not None else np.nan),
        'hora_ini': df[j_hi].map(a_hora), 'hora_fin': df[j_hf].map(a_hora) if j_hf is not None else np.nan,
        'creditos': pd.to_numeric(df[j_cre], errors='coerce') if j_cre is not None else np.nan,
        'tipologia': df[j_tip].map(norm) if j_tip is not None else np.nan,
        'ciclo': df[j_cic].map(norm) if j_cic is not None else np.nan,
        'fecha_ini': pd.to_datetime(df[j_fi], errors='coerce', dayfirst=True) if j_fi is not None else pd.NaT,
        'fecha_fin': pd.to_datetime(df[j_ff], errors='coerce', dayfirst=True) if j_ff is not None else pd.NaT,
        'tiene_docente': df[j_prof].notna() & ~df[j_prof].astype(str).str.strip().isin(['-','','nan']) if j_prof is not None else np.nan,
    })
    for d,j in jd.items():
        out[d] = df[j].astype(str).str.strip().str.upper().eq('X').astype(int) if j is not None else 0
    out['archivo'] = os.path.basename(ruta)
    # ciclo/semestre a partir del sufijo del nombre del grupo (p. ej. 'ALGEBRA LINEAL C4G1')
    out['ciclo'] = out['nombre_grupo'].astype(str).map(norm).str.extract(r'\b([CS]\d)G\d+\s*$')[0]
    return out

def unificar(carpeta):
    partes = []
    for f, per in PERIODOS.items():
        ruta = os.path.join(carpeta, f)
        for h in pd.ExcelFile(ruta).sheet_names:
            if h.strip() in FACULTADES:
                p = leer_hoja(ruta, h.strip() if h in pd.ExcelFile(ruta).sheet_names else h, per)
                if p is not None: partes.append(p)
    d = pd.concat(partes, ignore_index=True)
    return d

if __name__ == '__main__':
    d = unificar('datos_crudos')
    print(d.shape); print(d.groupby('periodo').size())
    print(d.isna().mean().round(3))
    print(d.head())
