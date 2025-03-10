from flask import Flask, request, jsonify
import os
import resource
from flask_cors import CORS
import pandas as pd
from sklearn.cluster import KMeans
import fileio

app = Flask(__name__)
CORS(app)

cluster_data = {
    "dataframe": None,
    "clusters": None,
    "column": None
}

def limit_memory(max_mem_bytes):
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (max_mem_bytes, hard))
    except Exception as e:
        print(f"Warning: Could not set memory limit: {e}")

# Limit to 6GB to stay safely under 7GB
limit_memory(6 * 1024 * 1024 * 1024)

@app.route('/')
def home():
    return "API is running"

@app.route("/vectorize", methods=["POST"])
def vectorize():
    try:
        file = request.files["file"]
        df = pd.read_csv(file) #type: ignore
        column = request.form.get("column")
        num_clusters = int(request.form.get("clusters", 0) or 0)

        if column not in df.columns:
            return jsonify({"error": f'CSV must contain a "{column}" column.'}), 400

        embeddings = fileio.get_embeddings(df[column].astype(str))

        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        cluster_data["dataframe"] = df
        cluster_data["clusters"] = clusters
        cluster_data["column"] = column

        # 1 seems to be good, 0 is bad
        # fileio.print_cluster_rows(df["text"].astype(str), clusters, 1)

        image_base64 = fileio.generate_umap_plot(embeddings, clusters)

        return jsonify({"clusters": clusters.tolist(), "umap_graph": image_base64}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clusters", methods=["POST"])
def returnRows():
    if any(value is None for value in cluster_data.values()):
        return jsonify({"error": "dataframe uninitialized"}), 400

    cluster_index = int(request.form.get("cluster"))

    try:
        filtered_rows = cluster_data["dataframe"][cluster_data["clusters"] == cluster_index]
        return jsonify({"clusters": filtered_rows.to_dict(orient="records")}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Starting server on port {port} with HOST='0.0.0.0'")
    app.run(host='0.0.0.0', port=port)
