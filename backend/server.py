from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer, BertModel
from flask_cors import CORS
import pandas as pd
from sklearn.cluster import KMeans
from umap import UMAP
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)


@app.route("/vectorize", methods=["POST"])
def vectorize():
    try:
        file = request.files["file"]
        df = pd.read_csv(file)

        if "text" not in df.columns:
            return jsonify({"error": 'CSV must contain a "text" column.'}), 400

        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        model = BertModel.from_pretrained("bert-base-uncased")

        def embed_text(text):
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

        embeddings = df["text"].astype(str).apply(embed_text).tolist()

        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        reducer = UMAP()
        embedding = reducer.fit_transform(embeddings)

        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(
            embedding[:, 0], embedding[:, 1], c=clusters, cmap="plasma", s=5
        )
        plt.colorbar(scatter, label="Cluster")

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")

        return jsonify({"clusters": clusters.tolist(), "umap_graph": image_base64}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
