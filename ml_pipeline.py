import os, re, json, joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

TEXT_COLUMNS = ["title", "company_profile", "description", "requirements", "benefits"]

def clean_text(x):
    x = "" if pd.isna(x) else str(x)
    x = x.lower()
    x = re.sub(r"http\S+|www\S+", " ", x)
    x = re.sub(r"[^a-z0-9\s]", " ", x)
    x = re.sub(r"\s+", " ", x).strip()
    return x

def detect_target(df):
    candidates = ["fraudulent", "fake", "is_fake", "label", "target", "scam", "class"]
    lower = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower:
            return lower[c]
    return None

def prepare_dataframe(path):
    df = pd.read_csv(path)
    target = detect_target(df)
    if not target:
        raise ValueError("Target column not found. Use a column named fraudulent, fake, label, target, scam or class.")

    available_text = [c for c in TEXT_COLUMNS if c in df.columns]
    if not available_text:
        # Fallback: use all object/string columns except target
        available_text = [c for c in df.columns if c != target and df[c].dtype == "object"]

    if not available_text:
        raise ValueError("No text columns found in the dataset.")

    df[available_text] = df[available_text].fillna("")
    df["combined_text"] = df[available_text].astype(str).agg(" ".join, axis=1).map(clean_text)

    # Remove rows without useful text
    df = df[df["combined_text"].str.len() > 0].copy()

    y = df[target]
    # Convert common textual labels to 0/1 where possible
    if y.dtype == "object":
        mapping = {}
        for val in y.dropna().unique():
            s = str(val).lower().strip()
            if s in ["fake", "fraud", "fraudulent", "scam", "1", "yes", "true"]:
                mapping[val] = 1
            elif s in ["real", "genuine", "legitimate", "not fraud", "0", "no", "false"]:
                mapping[val] = 0
        if mapping:
            y = y.map(mapping)
        else:
            y = pd.factorize(y)[0]
    y = pd.to_numeric(y, errors="coerce")
    valid = y.notna()
    return df.loc[valid], y.loc[valid].astype(int), target

def preprocess_dataset(path):
    df = pd.read_csv(path)
    before = len(df)
    df = df.drop_duplicates().copy()
    df = df.fillna("")
    df.to_csv("dataset/preprocessed_dataset.csv", index=False)
    return f"Preprocessing completed. Removed {before-len(df)} duplicate rows. Missing values filled."

def train_model(path):
    try:
        df, y, target = prepare_dataframe(path)
        if y.nunique() < 2:
            raise ValueError("Target column must contain at least two classes.")

        X_train, X_test, y_train, y_test = train_test_split(
            df["combined_text"], y, test_size=0.2, random_state=42, stratify=y
        )

        models = {
            "Logistic Regression": Pipeline([
                ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1,2), sublinear_tf=True)),
                ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
            ]),
            "Random Forest": Pipeline([
                ("tfidf", TfidfVectorizer(max_features=20000, ngram_range=(1,2)),
                ),
                ("clf", RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced"))
            ])
        }

        results = {}
        best_name, best_acc, best_model = None, -1, None

        for name, model in models.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            acc = accuracy_score(y_test, pred)
            results[name] = {
                "accuracy": round(acc*100, 2),
                "precision": round(precision_score(y_test, pred, zero_division=0)*100, 2),
                "recall": round(recall_score(y_test, pred, zero_division=0)*100, 2),
                "f1": round(f1_score(y_test, pred, zero_division=0)*100, 2),
                "confusion_matrix": confusion_matrix(y_test, pred).tolist()
            }
            if acc > best_acc:
                best_acc, best_name, best_model = acc, name, model

        joblib.dump(best_model, f"{MODEL_DIR}/scam_model.pkl")
        metadata = {
            "target_column": target,
            "best_model": best_name,
            "results": results,
            "training_rows": len(X_train),
            "testing_rows": len(X_test)
        }
        with open(f"{MODEL_DIR}/results.json", "w") as f:
            json.dump(metadata, f, indent=2)

        return metadata
    except Exception as e:
        return {"error": str(e)}

def predict_job(data):
    model_path = f"{MODEL_DIR}/scam_model.pkl"
    if not os.path.exists(model_path):
        return {"error": "Train the model first."}

    model = joblib.load(model_path)
    text = " ".join([data.get(c, "") for c in TEXT_COLUMNS])
    text = clean_text(text)

    pred = int(model.predict([text])[0])
    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(max(model.predict_proba([text])[0])) * 100

    if pred == 1:
        label, risk = "Potential Scam / Fake Job", "HIGH"
    else:
        label, risk = "Likely Genuine Job", "LOW"

    return {
        "label": label,
        "risk": risk,
        "confidence": round(probability, 2) if probability is not None else None
    }
