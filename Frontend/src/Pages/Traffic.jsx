import axios from "axios";
import { useState } from "react";

export default function TrafficPage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (selectedFiles.length !== 4) {
      alert("Please upload exactly 4 videos.");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("videos", file));

    try {
      setLoading(true);
      setResult(null); // clear previous result
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error uploading files:", error);
      setResult({ error: "Upload failed. Please try again later." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ position: "relative", minHeight: "100vh", backgroundColor: "#f3f4f6" }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `url("https://png.pngtree.com/thumb_back/fh260/background/20241210/pngtree-advanced-highway-with-ai-managed-traffic-flow-and-self-repairing-roads-image_16739858.jpg")`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(8px)",
          zIndex: 0,
        }}
      />
      <div style={{ position: "relative", zIndex: 10, padding: "1.5rem" }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            gap: "1.5rem",
            maxWidth: "96rem",
            margin: "0 auto",
          }}
        >
          {/* Left Panel */}
          <div
            style={{
              width: "50%",
              maxWidth: "50%",
              background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
              padding: "1.5rem",
              boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
              color: "white",
            }}
          >
            <section>
              <h2 style={{ fontSize: "1.25rem", fontWeight: "600", marginBottom: "0.5rem" }}>
                Enhance Traffic Efficiency Using AI
              </h2>
              <p>
                <p>
                  Just upload videos from a 4-lane intersection—our system will review the traffic
                  and recommend how long each green light should last.
                </p>
              </p>
            </section>

            <section style={{ marginTop: "2rem" }}>
              <form onSubmit={handleSubmit}>
                <label
                  htmlFor="video-upload"
                  style={{
                    display: "block",
                    width: "100%",
                    padding: "0.75rem",
                    backgroundColor: "#1f2937",
                    color: "white",
                    textAlign: "center",
                    fontWeight: "600",
                    border: "1px solid #ccc",
                    cursor: "pointer",
                    borderRadius: "6px",
                    marginBottom: "1rem",
                  }}
                >
                  CLICK TO UPLOAD TRAFFIC VIDEOS
                </label>

                <input
                  id="video-upload"
                  type="file"
                  multiple
                  accept="video/*"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                />

                <button
                  type="submit"
                  style={{
                    width: "100%",
                    background: "linear-gradient(135deg, #00ff87, #60efff)",
                    color: "black",
                    padding: "0.5rem",
                    fontWeight: "700",
                    border: "none",
                    cursor: "pointer",
                    borderRadius: "6px",
                  }}
                  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#dc2626")}
                  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#ef4444")}
                >
                  ANALYZE TRAFFIC FLOW
                </button>
              </form>
            </section>
          </div>

          {/* Right Panel */}
          <div
            style={{
              width: "50%",
              padding: "1.5rem",
              boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
              minHeight: "300px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              background: loading
                ? "linear-gradient(135deg, #2b5876, #4e4376)" // Dark gradient for loading
                : "linear-gradient(135deg, #0f2027, #203a43, #2c5364)", // Dark gradient for non-loading
              borderRadius: "10px", // Soft rounded corners for better aesthetics
              overflow: "hidden", // To make sure no elements spill out of bounds
            }}
          >
            {/* {loading && (
              <div style={{ display: "flex", gap: "1.5rem" }}>
                <div
                  style={{
                    width: "3rem",
                    height: "3rem",
                    borderRadius: "9999px",
                    backgroundColor: "#7f1d1d",
                    animation: "redGlow 3s infinite",
                  }}
                />
                <div
                  style={{
                    width: "3rem",
                    height: "3rem",
                    borderRadius: "9999px",
                    backgroundColor: "#78350f",
                    animation: "yellowGlow 3s infinite",
                  }}
                />
                <div
                  style={{
                    width: "3rem",
                    height: "3rem",
                    borderRadius: "9999px",
                    backgroundColor: "#064e3b",
                    animation: "greenGlow 3s infinite",
                  }}
                />
                <style>
                  {`
          @keyframes redGlow {
            0%, 33.33%, 100% { background-color: #7f1d1d; }
            16.66% { background-color: #ef4444; }
          }
          @keyframes yellowGlow {
            0%, 33.33%, 100% { background-color: #78350f; }
            49.99% { background-color: #facc15; }
          }
          @keyframes greenGlow {
            0%, 66.66%, 100% { background-color: #064e3b; }
            83.33% { background-color: #22c55e; }
          }
        `}
                </style>
              </div>
            )} */}

            {!loading && !result && (
              <p style={{ textAlign: "center", color: "white", fontSize: "1.125rem" }}>
                The results of the traffic signal optimization will be displayed here.
                <br />
              </p>
            )}

            {!loading && result?.error && (
              <div style={{ color: "white", fontWeight: "600", textAlign: "center" }}>
                <h3>Error:</h3>
                <p>{result.error}</p>
              </div>
            )}

            {!loading && result && !result.error && (
              <div style={{ color: "white" }}>
                <h2
                  style={{
                    fontSize: "1.25rem",
                    fontWeight: "bold",
                    color: "white",
                    marginBottom: "0.5rem",
                    textAlign: "center",
                  }}
                >
                  Traffic Signal Adjustment Recommendations (By Priority)
                </h2>
                <ul
                  style={{
                    listStyleType: "disc",
                    paddingLeft: "1.5rem",
                    paddingTop: "1.5rem",
                    lineHeight: "1.75rem",
                  }}
                >
                  {Object.entries(result)
                    .sort((a, b) => b[1].green_time - a[1].green_time) // Sort by green time descending
                    .map(([lane, { green_time, message }], index) => (
                      <li key={lane}>
                        PRIORITY {index + 1} - {lane.toUpperCase()} LANE:{" "}
                        <strong>{green_time}</strong> seconds
                        {message && (
                          <span style={{ color: "red", fontWeight: "bold" }}> ({message})</span>
                        )}
                      </li>
                    ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
