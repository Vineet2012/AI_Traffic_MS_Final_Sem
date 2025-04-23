import React from "react";
import "./cards.css";

export default function CardsCmp() {
  return (
    <div className="glass-container">
      <div className="glass-card">
        <h2 style={{ fontSize: "20px", fontWeight: "600" }}>Traffic Management System</h2>
        <p>This card has a blur and transparent glass effect.</p>
      </div>
    </div>
  );
}
