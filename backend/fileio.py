from transformers import BertTokenizer, BertModel
from umap import UMAP
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from tqdm import tqdm
import torch

def get_embeddings(text_series, batch_size=32, device=None):
    # Determine device (use GPU if available)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model and tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased").to(device)
    model.eval()  # Set to evaluation mode

    embeddings = []

    # Process in batches with progress bar
    for i in tqdm(range(0, len(text_series), batch_size)):
        batch_texts = text_series[i:i+batch_size].tolist()

        # Handle empty or None texts
        batch_texts = [str(text) if text is not None else "" for text in batch_texts]

        try:
            # Tokenize with attention masks
            inputs = tokenizer(batch_texts, return_tensors="pt", truncation=True,
                              padding=True, max_length=512)

            # Move inputs to device
            inputs = {key: val.to(device) for key, val in inputs.items()}

            # Process with no gradient calculation
            with torch.no_grad():
                outputs = model(**inputs)

            # Extract embeddings (mean of last hidden states)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            embeddings.extend(batch_embeddings)

        except Exception as e:
            print(f"Error processing batch {i}-{i+batch_size}: {e}")
            # Add empty embeddings for failed batch
            empty_embedding = np.zeros((len(batch_texts), model.config.hidden_size))
            embeddings.extend(empty_embedding)

    return embeddings

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
