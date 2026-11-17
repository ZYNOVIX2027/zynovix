from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZYNOVIX AI</title>
<style>
body {
    background:#080d18;
    color:white;
    font-family:Arial;
    padding:20px;
}
.box {
    max-width:450px;
    margin:auto;
    background:#141e30;
    padding:22px;
    border-radius:16px;
}
h1 {color:#00e5a0;text-align:center}
input,button {
    width:100%;
    padding:13px;
    margin:8px 0;
    border-radius:8px;
    border:none;
    box-sizing:border-box;
}
button {
    background:#00d99b;
    font-weight:bold;
}
.result {
    background:#202e43;
    padding:15px;
    margin-top:15px;
    border-radius:10px;
}
</style>
</head>
<body>
<div class="box">
<h1>⚡ ZYNOVIX AI</h1>
<p style="text-align:center">FOOTBALL PREDICTION ENGINE</p>

<form method="POST">
<input name="home" placeholder="Équipe domicile" required>
<input name="away" placeholder="Équipe extérieur" required>

<label>Buts attendus domicile</label>
<input type="number" name="lh" value="1.5"
step="0.1" min="0.1" max="5" required>

<label>Buts attendus extérieur</label>
<input type="number" name="la" value="1.1"
step="0.1" min="0.1" max="5" required>

<button type="submit">ANALYSER LE MATCH</button>
</form>

{% if result %}
<div class="result">
<h2>{{home}} - {{away}}</h2>
<h3>🏆 1X2</h3>
<p>Victoire domicile : {{result.h}}%</p>
<p>Match nul : {{result.d}}%</p>
<p>Victoire extérieur : {{result.a}}%</p>

<h3>🎯 Scores exacts probables</h3>
{% for score,p in result.scores %}
<p>{{score}} : {{p}}%</p>
{% endfor %}

<h3>⚽ Plus/Moins 2.5</h3>
<p>Over 2.5 : {{result.over}}%</p>
<p>Under 2.5 : {{result.under}}%</p>

<h3>🤝 BTTS</h3>
<p>Les deux équipes marquent : {{result.btts}}%</p>
</div>
{% endif %}

<p style="text-align:center;color:#8192a8">
ZYNOVIX AI © 2026
</p>
</div>
</body>
</html>
"""

def poisson(lam, k):
    return math.exp(-lam) * lam**k / math.factorial(k)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    home = ""
    away = ""

    if request.method == "POST":
        home = request.form["home"]
        away = request.form["away"]
        lh = float(request.form["lh"])
        la = float(request.form["la"])

        scores = []
        h = d = a = over = btts = 0

        for i in range(9):
            for j in range(9):
                p = poisson(lh, i) * poisson(la, j)

                if i > j:
                    h += p
                elif i == j:
                    d += p
                else:
                    a += p

                if i + j > 2:
                    over += p

                if i > 0 and j > 0:
                    btts += p

                scores.append((f"{i}-{j}", p))

        scores.sort(key=lambda x: x[1], reverse=True)

        result = {
            "h": round(h * 100, 1),
            "d": round(d * 100, 1),
            "a": round(a * 100, 1),
            "over": round(over * 100, 1),
            "under": round((1-over) * 100, 1),
            "btts": round(btts * 100, 1),
            "scores": [(s, round(p*100, 1))
                       for s, p in scores[:5]]
        }

    return render_template_string(
        HTML, result=result, home=home, away=away
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
