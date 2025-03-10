from transformers import BertTokenizer, BertModel
import gc
from umap import UMAP
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import nump

def get_embeddings(text_series):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    def embed_text(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

    return text_series.apply(embed_text).tolist()


def generate_umap_plot(embeddings, clusters):
    reducer = UMAP(n_neighbors=15, min_dist=0.1, n_components=2,
                   metric='euclidean', low_memory=True)
    embedding = reducer.fit_transform(embeddings)
    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype(np.float32)

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
