from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os, pandas as pd
from werkzeug.utils import secure_filename
from ml_pipeline import train_model, preprocess_dataset, predict_job

app = Flask(__name__)
app.secret_key = "recruitment-scam-demo-key"

UPLOAD_FOLDER = "dataset"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("models", exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("dataset")
        if not file or file.filename == "":
            flash("Please select a CSV file.", "danger")
            return redirect(url_for("upload"))
        if not allowed_file(file.filename):
            flash("Only CSV files are allowed.", "danger")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        df = pd.read_csv(path)
        df.to_csv("dataset/current_dataset.csv", index=False)
        flash(f"Dataset uploaded successfully: {filename}", "success")
        return redirect(url_for("preprocess"))

    return render_template("upload.html")

@app.route("/preprocess")
def preprocess():
    path = "dataset/current_dataset.csv"
    if not os.path.exists(path):
        return render_template("preprocess.html", error="Upload a dataset first.")
    df = pd.read_csv(path)
    info = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "column_names": list(df.columns)
    }
    return render_template("preprocess.html", info=info)

@app.route("/run-preprocess", methods=["POST"])
def run_preprocess():
    path = "dataset/current_dataset.csv"
    if not os.path.exists(path):
        flash("Upload a dataset first.", "danger")
    else:
        result = preprocess_dataset(path)
        flash(result, "success")
    return redirect(url_for("preprocess"))

@app.route("/visualization")
def visualization():
    path = "dataset/current_dataset.csv"
    if not os.path.exists(path):
        return render_template("visualization.html", error="Upload a dataset first.")
    df = pd.read_csv(path)
    target = find_target(df)
    counts = {}
    if target:
        vc = df[target].astype(str).value_counts()
        counts = {"labels": vc.index.tolist(), "values": vc.values.tolist()}
    return render_template("visualization.html", counts=counts, target=target)

@app.route("/train", methods=["GET", "POST"])
def train():
    result = None
    if request.method == "POST":
        path = "dataset/current_dataset.csv"
        if not os.path.exists(path):
            flash("Upload a dataset first.", "danger")
        else:
            result = train_model(path)
    return render_template("train.html", result=result)

@app.route("/detect", methods=["GET", "POST"])
def detect():
    prediction = None
    if request.method == "POST":
        data = {
            "title": request.form.get("title", ""),
            "company_profile": request.form.get("company_profile", ""),
            "description": request.form.get("description", ""),
            "requirements": request.form.get("requirements", ""),
            "benefits": request.form.get("benefits", "")
        }
        prediction = predict_job(data)
    return render_template("detect.html", prediction=prediction)

@app.route("/results")
def results():
    result = None
    if os.path.exists("models/results.json"):
        with open("models/results.json", "r") as f:
            result = json.load(f)
    return render_template("results.html", result=result)

def find_target(df):
    candidates = ["fraudulent", "fake", "is_fake", "label", "target", "scam", "class"]
    lower = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower:
            return lower[c]
    return None

if __name__ == "__main__":
    app.run(debug=True)
