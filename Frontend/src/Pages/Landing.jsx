import { useNavigate } from "react-router-dom";
import CardsCmp from "./cards";

export default function LandingPage() {
  // const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  const handleEnter = () => {
    navigate("/traffic");
  };

  // const handleVideoLoad = () => {
  //   setIsLoading(false);
  // };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        position: "relative",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      <video
        autoPlay
        loop
        muted
        playsInline
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          filter: "blur(6px)",
          zIndex: -2,
        }}
      >
        <source
          src="https://videos.pexels.com/video-files/2053855/2053855-uhd_2560_1440_30fps.mp4"
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>

      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "rgba(0, 0, 0, 0.4)",
          zIndex: -1,
        }}
      />

      <div style={{ zIndex: 1, textAlign: "center", color: "white" }}>
        <p
          style={{
            fontSize: "40px",
            fontFamily: "sans-serif",
            fontWeight: "600",
            marginTop: "64px",
          }}
        >
          AI TRAFFIC MANAGEMENT SYSTEM
        </p>

        <div style={{ display: "flex", columnGap: "40px", marginTop: "104px" }}>
          <CardsCmp />
          <CardsCmp />
          <CardsCmp />
        </div>

        <div style={{ marginTop: "104px" }}>
          <button
            onClick={handleEnter}
            className="px-8 py-4 text-lg font-bold text-white rounded-xl transition duration-300 shadow-lg"
            style={{
              background: "rgba(255, 255, 255, 0.1)",
              backdropFilter: "blur(6px)",
              border: "2px solid rgba(255, 255, 255, 0.2)",
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
              cursor: "pointer",
            }}
          >
            Analyze Traffic Flow
          </button>
        </div>
      </div>
    </div>
  );
}
