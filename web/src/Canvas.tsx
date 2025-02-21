import { useRef, useEffect } from "react";

function Canvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;

    ctx.scale(dpr, dpr);

    ctx.fillStyle = "blue";

    ctx.fillRect(50, 50, 50, 50);
  });
  return <canvas ref={canvasRef} className="h-full w-full"></canvas>;
}
export default Canvas;
