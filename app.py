from flask import Flask, Response, render_template_string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import patheffects
import random
import io

app = application = Flask(__name__)

# ==========================================================
# DATOS BAJÍO
# ==========================================================
frecuencias_bajio = [10,7,7,7,7,7,5]

intervalos_bajio = [
    "4.5-9.9",
    "9.9-15.3",
    "15.3-20.7",
    "20.7-26.1",
    "26.1-31.5",
    "31.5-36.9",
    "36.9-42.3"
]

# ==========================================================
# DATOS SUR
# ==========================================================
frecuencias_sur = [5,7,7,8,9,7,7]

intervalos_sur = [
    "21.8-22.5",
    "22.5-23.2",
    "23.2-23.9",
    "23.9-24.6",
    "24.6-25.3",
    "25.3-26.0",
    "26.0-26.7"
]

# ==========================================================
# PALETA
# ==========================================================
paleta = [
    "#00E5FF",
    "#FF00FF",
    "#00FFB3",
    "#FFD60A",
    "#9D4EDD",
    "#3A86FF",
    "#FF006E"
]

# ==========================================================
# FUNCIÓN HISTOGRAMA
# ==========================================================
def crear_histograma(ax, frecuencias, intervalos, titulo):

    ax.set_facecolor("#081120")

    x = np.arange(len(frecuencias))

    fr = np.array(frecuencias) / sum(frecuencias)

    porcentajes = fr * 100

    ax.set_ylim(0,12)

    # ======================================================
    # BARRAS
    # ======================================================
    barras = ax.bar(
        x,
        frecuencias,
        width=0.75,
        color=paleta[:len(frecuencias)],
        edgecolor="white",
        linewidth=2.5,
        zorder=5
    )

    # ======================================================
    # EFECTO GLOW
    # ======================================================
    for barra in barras:

        barra.set_path_effects([
            patheffects.withStroke(
                linewidth=12,
                foreground='white',
                alpha=0.08
            )
        ])

    # ======================================================
    # TÍTULO
    # ======================================================
    titulo_ax = ax.set_title(
        titulo,
        fontsize=26,
        color="white",
        fontweight='bold',
        pad=20
    )

    titulo_ax.set_path_effects([
        patheffects.withStroke(
            linewidth=8,
            foreground='#00E5FF',
            alpha=0.6
        )
    ])

    # ======================================================
    # EJES
    # ======================================================
    ax.set_xlabel(
        "INTERVALOS DE CLASE",
        fontsize=13,
        color="white",
        fontweight='bold'
    )

    ax.set_ylabel(
        "FRECUENCIA ABSOLUTA (f)",
        fontsize=13,
        color="white",
        fontweight='bold'
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        intervalos,
        rotation=15,
        fontsize=10,
        color='white'
    )

    ax.tick_params(colors='white')

    ax.grid(
        True,
        linestyle=':',
        linewidth=1,
        color='#00E5FF',
        alpha=0.18
    )

    # ======================================================
    # LÍNEA SUPERIOR
    # ======================================================
    linea, = ax.plot(
        x,
        np.array(frecuencias) + 0.2,
        color="#FF3131",
        linewidth=4,
        marker='o',
        markersize=12,
        zorder=10
    )

    linea.set_path_effects([
        patheffects.withStroke(
            linewidth=10,
            foreground='#FF0000',
            alpha=0.3
        )
    ])

    # ======================================================
    # ETIQUETAS
    # ======================================================
    textos = []

    for i in range(len(frecuencias)):

        # FRECUENCIA
        txt1 = ax.text(
            x[i],
            frecuencias[i] + 0.5,
            f"{frecuencias[i]}",
            ha='center',
            fontsize=14,
            color='white',
            fontweight='bold'
        )

        txt1.set_path_effects([
            patheffects.withStroke(
                linewidth=5,
                foreground='black'
            )
        ])

        textos.append(txt1)

        # FRECUENCIA RELATIVA
        txt2 = ax.text(
            x[i],
            frecuencias[i]*0.55,
            f"Fr={fr[i]:.2f}",
            ha='center',
            fontsize=10,
            color='#FFD60A',
            fontweight='bold'
        )

        textos.append(txt2)

        # PORCENTAJE
        txt3 = ax.text(
            x[i],
            frecuencias[i]*0.25,
            f"{porcentajes[i]:.1f}%",
            ha='center',
            fontsize=9,
            color='white'
        )

        textos.append(txt3)

    return barras, linea


def generar_gif():
    # ==========================================================
    # FIGURA
    # ==========================================================
    fig, axs = plt.subplots(1,2, figsize=(24,10))

    fig.patch.set_facecolor("#030712")

    # ==========================================================
    # ESTRELLAS
    # ==========================================================
    estrellas = []

    for _ in range(350):

        estrella = fig.text(
            random.uniform(0,1),
            random.uniform(0,1),
            random.choice(["✦","•","✧"]),
            color=random.choice([
                "#FFFFFF",
                "#00E5FF",
                "#FFD60A",
                "#FF61F6"
            ]),
            fontsize=random.uniform(4,12),
            alpha=random.uniform(0.1,0.9)
        )

        estrellas.append(estrella)

    # ==========================================================
    # CREAR GRÁFICAS
    # ==========================================================
    barras1, linea1 = crear_histograma(
        axs[0],
        frecuencias_bajio,
        intervalos_bajio,
        "🌌 REGIÓN DEL BAJÍO"
    )

    barras2, linea2 = crear_histograma(
        axs[1],
        frecuencias_sur,
        intervalos_sur,
        "🚀 REGIÓN DEL SUR"
    )

    # ==========================================================
    # ANIMACIÓN GLOBAL
    # ==========================================================
    def animar(frame):

        # ======================================================
        # ANIMAR ESTRELLAS
        # ======================================================
        for estrella in estrellas:

            estrella.set_alpha(
                random.uniform(0.1,1)
            )

        # ======================================================
        # CAMBIO DE COLORES BARRAS
        # ======================================================
        for barras in [barras1, barras2]:

            for barra in barras:

                barra.set_color(
                    random.choice(paleta)
                )

        # ======================================================
        # EFECTO PULSO
        # ======================================================
        for barras in [barras1, barras2]:

            for barra in barras:

                altura = barra.get_height()

                pulso = np.sin(frame/8) * 0.15

                barra.set_height(
                    altura + pulso
                )

        # ======================================================
        # CAMBIO COLOR LÍNEAS
        # ======================================================
        linea1.set_color(random.choice(paleta))
        linea2.set_color(random.choice(paleta))

    # ==========================================================
    # ANIMACIÓN
    # ==========================================================
    ani = FuncAnimation(
        fig,
        animar,
        frames=20,
        interval=400,
        cache_frame_data=False
    )

    # ==========================================================
    # TÍTULO PRINCIPAL
    # ==========================================================
    titulo = fig.suptitle(
        "📊 HISTOGRAMAS ESTADÍSTICOS FUTURISTAS 📊",
        fontsize=32,
        color="white",
        fontweight='bold'
    )

    titulo.set_path_effects([
        patheffects.withStroke(
            linewidth=10,
            foreground='#00E5FF',
            alpha=0.7
        )
    ])

    # ==========================================================
    # PIE
    # ==========================================================
    fig.text(
        0.5,
        0.02,
        "✨ FRECUENCIA ABSOLUTA • FRECUENCIA RELATIVA • PORCENTAJES • INTERVALOS DE CLASE ✨",
        ha='center',
        color='#00E5FF',
        fontsize=13,
        fontweight='bold'
    )

    plt.tight_layout(rect=[0,0.05,1,0.95])

    buf = io.BytesIO()
    ani.save(buf, writer='pillow', fps=2.5)
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ==========================================================
# PÁGINA HTML
# ==========================================================
HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Histogramas Estadísticos Futuristas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #030712;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }
        h1 {
            font-size: clamp(1rem, 3vw, 1.8rem);
            color: #00E5FF;
            text-align: center;
            margin-bottom: 1.5rem;
            text-shadow: 0 0 20px #00E5FF88;
            padding: 0 1rem;
        }
        .gif-container {
            border: 2px solid #00E5FF44;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 40px #00E5FF22;
            max-width: 98vw;
        }
        img {
            display: block;
            max-width: 100%;
            height: auto;
        }
        p {
            margin-top: 1rem;
            color: #00E5FF99;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <h1>📊 Histogramas Estadísticos Futuristas 📊</h1>
    <div class="gif-container">
        <img src="/animation" alt="Histogramas animados futuristas">
    </div>
    <p>✨ Frecuencia Absoluta • Frecuencia Relativa • Porcentajes • Intervalos de Clase ✨</p>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/animation")
def animation():
    gif_bytes = generar_gif()
    return Response(gif_bytes, mimetype="image/gif")


if __name__ == "__main__":
    app.run(debug=True)