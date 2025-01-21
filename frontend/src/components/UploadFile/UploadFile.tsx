import { useState } from "react";
import axios from "axios";
import Spinner from "../Spinner/Spinner";

function FileUploader() {
  const [file, setFile] = useState(null);
  const [vectors, setVectors] = useState([]);
  const [image, setImage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: any) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    console.log(formData)

    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/vectorize",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        },
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
      <button onClick={handleSubmit}>Upload and Vectorize</button>
      {loading ? (
        <Spinner />
      ) : (
        <>
          {error && <p className="text-red-500">{error}</p>}
          {vectors.length > 0 && (
            <div>
              <h2 className="pb-4">Vectorization Results</h2>
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
