import { useState } from "react";
import axios from "axios";
import Spinner from "../Spinner/Spinner";

function FileUploader() {
  const [file, setFile] = useState(null);
  const [columnName, setColumnName] = useState("");
  const [numClusters, setNumClusters] = useState("");
  const [vectors, setVectors] = useState([]);
  const [image, setImage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: any) => {
    setFile(event.target.files[0]);
  };

  const handleColumnNameChange = (event: any) => {
    setColumnName(event.target.value);
  };

  const handleNumClustersChange = (event: any) => {
    setNumClusters(event.target.value);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("column", columnName);
    formData.append("clusters", numClusters);

    setLoading(true);
    try {
      const response = await axios.post(
        "https://csvanalysis-production-46ec.up.railway.app/vectorize",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setVectors(response.data.clusters);
      setImage(response.data.umap_graph);
      setError("");
    } catch (err: any) {
      setError(err.response?.data?.error || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="bg-teal-600 rounded-3xl mb-4 p-4">CSV Analyzer</h1>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <input
        type="text"
        className="mr-4 text-center"
        placeholder="Column name to vectorize"
        value={columnName}
        onChange={handleColumnNameChange}
      />
      <input
        type="text"
        className="text-center"
        placeholder="Number of clusters"
        value={numClusters}
        onChange={handleNumClustersChange}
      />
      <div className="mb-4"></div>
      <button className="mb-2" onClick={handleSubmit}>Upload and Vectorize</button>
      {loading ? (
        <Spinner />
      ) : (
        <>
          {error && <p className="text-red-500">{error}</p>}
          {vectors.length > 0 && (
            <div>
              {image && (
                <div>
                  <img src={`data:image/png;base64,${image}`} alt="UMAP Graph" />
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default FileUploader;
