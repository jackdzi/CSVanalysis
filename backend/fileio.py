from transformers import BertTokenizer, BertModel
from umap import UMAP
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_embeddings(text_series):
    print("Embedding")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    def embed_text(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

    return text_series.apply(embed_text).tolist()

def generate_umap_plot(embeddings, clusters):
    reducer = UMAP()
    embedding = reducer.fit_transform(embeddings)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        embedding[:, 0], embedding[:, 1], c=clusters, cmap="cividis", s=5 #type: ignore
    )
    plt.colorbar(scatter, label="Cluster")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def print_cluster_rows(text_series, clusters, cluster_id):
    for text, cluster in zip(text_series, clusters):
        if cluster == cluster_id:
            print(text)
