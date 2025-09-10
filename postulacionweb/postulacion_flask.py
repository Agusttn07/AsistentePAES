from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# ===== Utilidades =====
def safe_int(x):
    try:
        return int(str(x).strip())
    except:
        return None

def clamp_0_1000(x):
    if x is None or x == "":
        return None
    try:
        v = float(x)
        if v < 0: return 0.0
        if v > 1000: return 1000.0
        return v
    except:
        return None

# ===== Carga de carreras =====
def cargar_ponderaciones():
    data = [
        {"universidad": "Universidad de Chile", "carrera": "Ingeniería y Ciencias (Plan Común)", "sede": "Santiago"},
        {"universidad": "Universidad de Chile", "carrera": "Medicina", "sede": "Santiago"},
        {"universidad": "Universidad de Chile", "carrera": "Derecho", "sede": "Santiago"},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Medicina", "sede": "Santiago"},
        {"universidad": "Universidad de Concepción", "carrera": "Medicina", "sede": "Concepción"},
        # ... puedes completar con todas tus universidades y carreras
    ]
    return pd.DataFrame(data)

ponderaciones_df = cargar_ponderaciones()

@app.route('/')
def index():
    universidades = sorted(ponderaciones_df["universidad"].unique())
    return render_template("index.html", universidades=universidades)

@app.route('/carreras', methods=['POST'])
def carreras():
    uni = request.json.get("universidad")
    carreras = sorted(ponderaciones_df.loc[ponderaciones_df["universidad"]==uni, "carrera"].unique())
    return jsonify(carreras)

@app.route('/sedes', methods=['POST'])
def sedes():
    uni = request.json.get("universidad")
    car = request.json.get("carrera")
    sedes = sorted(ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car), "sede"].unique())
    return jsonify(sedes)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    nem = clamp_0_1000(data.get("nem"))
    ranking = clamp_0_1000(data.get("ranking"))
    cl = clamp_0_1000(data.get("cl"))
    m1 = clamp_0_1000(data.get("m1"))
    m2 = clamp_0_1000(data.get("m2"))
    cs = clamp_0_1000(data.get("cs"))
    hs = clamp_0_1000(data.get("hs"))
    corte = clamp_0_1000(data.get("corte"))
    opcion_ch = data.get("opcion_ch")
    p_nem = data.get("p_nem",0)
    p_rank = data.get("p_rank",0)
    p_lec = data.get("p_lec",0)
    p_m1 = data.get("p_m1",0)
    p_m2 = data.get("p_m2",0)
    p_cie = data.get("p_cie",0)
    p_his = data.get("p_his",0)

    opt_cie = cs if opcion_ch=="Ciencias" else 0
    opt_his = hs if opcion_ch=="Historia" else 0
    p_opt_cie = p_cie if opcion_ch=="Ciencias" else 0
    p_opt_his = p_his if opcion_ch=="Historia" else 0

    ptotal = (
        nem * p_nem/100 + ranking * p_rank/100 + cl * p_lec/100 +
        m1 * p_m1/100 + m2 * p_m2/100 +
        opt_cie * p_opt_cie/100 + opt_his * p_opt_his/100
    )
    progreso = min((ptotal / corte) * 100, 100)

    resultado = {
        "ptotal": round(ptotal,2),
        "sobre_corte": ptotal >= corte,
        "diferencia": round(abs(ptotal-corte),2),
        "progreso": round(progreso,1)
    }
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
