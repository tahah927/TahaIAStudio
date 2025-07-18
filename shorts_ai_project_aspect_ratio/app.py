from flask import Flask, render_template, request
from moviepy import TextClip
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    generado = False
    nombre_video = ""

    if request.method == "POST":
        texto = request.form.get("texto", "Texto de ejemplo")
        
        # Crear clip de texto
        clip = TextClip(txt=texto, color='white', size=(1280, 720))
        clip = clip.set_duration(5)

        # Crear carpeta static si no existe
        os.makedirs("static", exist_ok=True)

        # Nombre único para el video
        nombre_video = f"{uuid.uuid4().hex}.mp4"
        output_path = os.path.join("static", nombre_video)

        # Guardar video
        clip.write_videofile(output_path, fps=24, codec='libx264')

        generado = True

    return render_template("index.html", generado=generado, video=nombre_video)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
