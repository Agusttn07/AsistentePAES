<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Asistente de Postulaciones 🎓</title>
</head>
<body>
    <h1>Asistente de Postulaciones 🎓</h1>

    <h3>Datos del postulante</h3>
    <input type="text" id="nombre" placeholder="Nombre">
    <input type="text" id="curso" placeholder="Curso"><br><br>

    <h3>Universidad y Carrera</h3>
    <select id="universidad"></select>
    <select id="carrera"></select>
    <select id="sede"></select><br><br>

    <h3>Puntajes PAES</h3>
    NEM: <input type="number" id="nem" value="100"><br>
    Ranking: <input type="number" id="ranking" value="100"><br>
    Lectora: <input type="number" id="cl" value="100"><br>
    M1: <input type="number" id="m1" value="100"><br>
    M2: <input type="number" id="m2" value="0"><br>
    Prueba Electiva:
    <select id="opcion_ch">
        <option value="Ciencias">Ciencias</option>
        <option value="Historia">Historia</option>
    </select><br>
    Ciencias: <input type="number" id="cs" value="0"><br>
    Historia: <input type="number" id="hs" value="0"><br>
    Puntaje corte: <input type="number" id="corte" value="500"><br><br>

    <h3>Ponderaciones (%)</h3>
    NEM: <input type="number" id="p_nem" value="0"><br>
    Ranking: <input type="number" id="p_rank" value="0"><br>
    Lectora: <input type="number" id="p_lec" value="0"><br>
    M1: <input type="number" id="p_m1" value="0"><br>
    M2: <input type="number" id="p_m2" value="0"><br>
    Ciencias: <input type="number" id="p_cie" value="0"><br>
    Historia: <input type="number" id="p_his" value="0"><br><br>

    <button onclick="calcular()">PONDERAR</button>

    <h3>Resultado</h3>
    <div id="resultado"></div>

    <script>
        const universidades = {{ universidades|tojson }};
        const uniSelect = document.getElementById("universidad");
        universidades.forEach(u => {
            const opt = document.createElement("option");
            opt.value = u;
            opt.text = u;
            uniSelect.add(opt);
        });

        uniSelect.addEventListener("change", async () => {
            const res = await fetch("/carreras", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({universidad: uniSelect.value})
            });
            const carreras = await res.json();
            const carreraSelect = document.getElementById("carrera");
            carreraSelect.innerHTML = "";
            carreras.forEach(c => {
                const opt = document.createElement("option");
                opt.value = c;
                opt.text = c;
                carreraSelect.add(opt);
            });
        });

        async function calcular() {
            const data = {
                nombre: document.getElementById("nombre").value,
                curso: document.getElementById("curso").value,
                universidad: document.getElementById("universidad").value,
                carrera: document.getElementById("carrera").value,
                sede: document.getElementById("sede").value,
                nem: parseFloat(document.getElementById("nem").value),
                ranking: parseFloat(document.getElementById("ranking").value),
                cl: parseFloat(document.getElementById("cl").value),
                m1: parseFloat(document.getElementById("m1").value),
                m2: parseFloat(document.getElementById("m2").value),
                cs: parseFloat(document.getElementById("cs").value),
                hs: parseFloat(document.getElementById("hs").value),
                corte: parseFloat(document.getElementById("corte").value),
                opcion_ch: document.getElementById("opcion_ch").value,
                p_nem: parseFloat(document.getElementById("p_nem").value),
                p_rank: parseFloat(document.getElementById("p_rank").value),
                p_lec: parseFloat(document.getElementById("p_lec").value),
                p_m1: parseFloat(document.getElementById("p_m1").value),
                p_m2: parseFloat(document.getElementById("p_m2").value),
                p_cie: parseFloat(document.getElementById("p_cie").value),
                p_his: parseFloat(document.getElementById("p_his").value)
            };
            const res = await fetch("/calcular", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
            const resultado = await res.json();
            let html = `Puntaje ponderado: ${resultado.ptotal}<br>`;
            if (resultado.sobre_corte) {
                html += `Estás sobre el corte por ${resultado.diferencia} puntos (${resultado.progreso}% del corte).`;
            } else {
                html += `No alcanzas el corte (${resultado.diferencia} puntos debajo, progreso: ${resultado.progreso}%).`;
            }
            document.getElementById("resultado").innerHTML = html;
        }
    </script>
</body>
</html>
