export function AnimatedBackground() {
  return (
    <div className="pointer-events-none absolute inset-0">
      <div className="cyber-grid-container">
        <div className="cyber-grid-plane" />
        <div className="voxel" style={{ left: "12%", top: "20%", animationDelay: "0s" }} />
        <div className="voxel" style={{ left: "80%", top: "18%", animationDelay: "2s" }} />
        <div className="voxel" style={{ left: "18%", top: "72%", animationDelay: "4s" }} />
        <div className="voxel" style={{ left: "85%", top: "60%", animationDelay: "1s" }} />
        <div className="voxel" style={{ left: "52%", top: "82%", animationDelay: "3s" }} />
      </div>
    </div>
  );
}
