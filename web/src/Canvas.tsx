import { useRef, useEffect, useState } from "react";

function Canvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const [scale, setScale] = useState(1);
  const [offsetX, setOffsetX] = useState(0);
  const [offsetY, setOffsetY] = useState(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;

    ctx.setTransform(scale * dpr, 0, 0, scale * dpr, offsetX, offsetY);

    ctx.fillStyle = "blue";

    ctx.fillRect(50, 50, 50, 50);
  });
  return (
    <canvas
      ref={canvasRef}
      className="h-full w-full"
      onWheel={(e) => {
        console.log(e.deltaY);
        setScale(scale * (1 + e.deltaY / 1000));
      }}
      onMouseDown={(e) => {
        setDragStart({ x: e.clientX, y: e.clientY });
        setIsDragging(!isDragging);
      }}
      onMouseUp={() => {
        setIsDragging(false);
      }}
      onMouseMove={(e) => {
        const dpr = window.devicePixelRatio || 1;
        if (isDragging) {
          setOffsetX(-(dragStart.x - e.clientX) * dpr);
          setOffsetY(-(dragStart.y - e.clientY) * dpr);
        }
      }}
    ></canvas>
  );
}
export default Canvas;
