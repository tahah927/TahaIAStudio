from flask import Flask, render_template, request, send_file
from moviepy import TextClip, CompositeVideoClip
import os
import uuid

app = Flask(__name__)

# Ruta para la página principal
@app.route("/", methods=["GET", "POST"])
def index():
    generado = False
    nombre_video = ""

    if request.method == "POST":
        texto = request.form.get("texto", "Texto de ejemplo")
        nombre_video = f"{uuid.uuid4().hex}.mp4"

        # Crear clip de texto
        clip = TextClip(texto, fontsize=70, color='white', size=(1280, 720))
        clip = clip.set_duration(5).set_position("center").on_color(color=(0, 0, 0))

        # Guardar el video
        output_path = os.path.join("static", nombre_video)
        clip.write_videofile(output_path, fps=24)

        generado = True

    return render_template("index.html", generado=generado, video=nombre_video)

# Ruta para descargar el video si se desea
@app.route("/descargar/<nombre>")
def descargar(nombre):
    return send_file(os.path.join("static", nombre), as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
