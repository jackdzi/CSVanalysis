import { useState } from "react";
import axios from "axios";

function GetCluster() {
  const [clusterName, setClusterName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [response, setResponse] = useState<any[]>([]);

  const handleClusterNameChange = (event: any) => {
    setClusterName(event.target.value);
  };

  const handleSubmit = async () => {

    const formData = new FormData();
    formData.append("cluster", clusterName);
    setLoading(true);

    try {
      const response = await axios.post(
        "http://10.223.131.34:10000/clusters",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResponse(response.data.clusters);
      setError("");
    } catch (err: any) {
      setError(err.response?.data?.error || "An error occurred.");
      setResponse([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="bg-teal-600 text-white rounded-3xl mb-4 p-4 text-xl font-bold text-center">
        Show Cluster Data
      </h1>

      <div className="flex flex-col gap-4">
        <div className="flex gap-4 items-center">
          <input
            type="text"
            className="border rounded p-2 flex-grow"
            placeholder="Cluster number (0-indexed)"
            value={clusterName}
            onChange={handleClusterNameChange}
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700 disabled:bg-teal-300 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : "Submit"}
          </button>
        </div>

        {error && (
          <div className="text-red-500 p-2 rounded bg-red-50">
            {error}
          </div>
        )}

        {response && (
          <div className="mt-4">
            <h2 className="font-semibold mb-2">Response:</h2>
            <pre className="bg-gray-100 text-black p-4 rounded overflow-auto whitespace-pre-wrap">
              {response.map((item: { text: string }) => (
                <div key={item.text}>
                  <p>{item.text}</p>
                  <br />
                </div>
              ))}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default GetCluster;
