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
          src="https://videos.pexels.com/video-files/31651707/13485024_1440_2560_30fps.mp4"
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

      {/* <div className="relative flex flex-col md:flex-row h-screen w-full">
        <div className="w-full md:w-1/2 flex flex-col justify-center px-6 md:px-12 space-y-6 relative">
          <div className="text-4xl md:text-6xl font-bold text-red-500 font-winky">
            AI BASED TRAFFIC MANAGEMENT SYSTEM
          </div>

          <p className="text-lg md:text-[20px] max-w-xl leading-relaxed text-white font-semibold">
            Our system leverages AI-powered object detection to monitor and optimize real-time traffic flow using computer vision.
          </p>

          <div className="mt-4">
            <h3 className="text-xl font-bold mb-2 text-red-600">How It Works</h3>
            <ul className="list-disc ml-5 space-y-1 text-white">
              <li>Upload videos showing 4 lanes at an intersection.</li>
              <li>AI model analyzes traffic congestion using computer vision.</li>
              <li>Gives higher priority to lanes with emergency vehicles.</li>
              <li>Suggests optimized green signal durations for all directions.</li>
            </ul>
          </div>

          <div className="flex justify-center my-5">
            <button
              onClick={handleEnter}
              className="px-8 py-4 bg-red-500 hover:bg-red-600 cursor-pointer text-lg font-bold text-white rounded-xl transition duration-300 shadow-lg"
            >
              Enter System
            </button>
          </div>
        </div>

        <div className="w-full md:w-1/2 relative">
          {isLoading && (
            <div className="absolute inset-0 flex justify-center items-center bg-gray-200 bg-opacity-50">
              <div className="border-t-4 border-red-500 border-solid w-16 h-16 rounded-full animate-spin"></div>
            </div>
          )}
          <video
            className="w-full h-full object-cover"
            autoPlay
            loop
            muted
            playsInline
            onLoadedData={handleVideoLoad} 
          >
            <source src={demo_video} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      </div> */}
    </div>
  );
}
