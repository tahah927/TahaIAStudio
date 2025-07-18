from flask import Flask, render_template, request, send_from_directory
from moviepy.editor import TextClip, CompositeVideoClip
import os

app = Flask(__name__)

def crear_video(tema, formato="mp4", duracion=15, aspecto="9:16"):
    os.makedirs("static", exist_ok=True)

    if aspecto == "9:16":
        width, height = 480, 854
    elif aspecto == "16:9":
        width, height = 854, 480
    elif aspecto == "1:1":
        width, height = 640, 640
    else:
        width, height = 480, 854

    texto = f"Tema: {tema}"
    txt_clip = TextClip(txt=texto, fontsize=40, color='white', size=(width, height), method='caption', bg_color='black')
    txt_clip = txt_clip.set_duration(duracion)

    video = CompositeVideoClip([txt_clip])

    ruta = f"static/video_short.{formato}"
    video.write_videofile(ruta, fps=24, codec='libx264', audio=False)

    return ruta

@app.route("/", methods=["GET", "POST"])
def index():
    generado = False
    formato = "mp4"
    if request.method == "POST":
        tema = request.form.get("tema")
        formato = request.form.get("formato", "mp4")
        duracion = int(request.form.get("duracion", 15))
        aspecto = request.form.get("aspecto", "9:16")

        if tema:
            crear_video(tema, formato=formato, duracion=duracion, aspecto=aspecto)
            generado = True

    return render_template("index.html", generado=generado, formato=formato)

@app.route("/video")
def video():
    formato = request.args.get("formato", "mp4")
    return send_from_directory("static", f"video_short.{formato}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
