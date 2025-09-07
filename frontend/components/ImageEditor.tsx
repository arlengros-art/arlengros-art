import React, { useRef, useState, useEffect } from 'react';

type Props = {
  src: string;
  onSubmit: (image: Blob, mask: Blob, prompt: string, mode: 'inpaint' | 'outpaint') => void;
};

const ImageEditor: React.FC<Props> = ({ src, onSubmit }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [prompt, setPrompt] = useState('');

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.src = src;
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx?.drawImage(img, 0, 0);
      };
    }
  }, [src]);

  const getPos = (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  };

  const startDraw = (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>) => {
    setIsDrawing(true);
    draw(e);
  };

  const endDraw = () => setIsDrawing(false);

  const draw = (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!ctx || !canvas) return;
    const { x, y } = getPos(e);
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, Math.PI * 2);
    ctx.fill();
  };

  const handleClick = (mode: 'inpaint' | 'outpaint') => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.toBlob((maskBlob) => {
      fetch(src)
        .then((r) => r.blob())
        .then((imgBlob) => {
          if (maskBlob) {
            onSubmit(imgBlob, maskBlob, prompt, mode);
          }
        });
    });
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        onMouseDown={startDraw}
        onMouseUp={endDraw}
        onMouseMove={draw}
        style={{ border: '1px solid #000' }}
      />
      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Prompt"
      />
      <button onClick={() => handleClick('inpaint')}>Inpaint</button>
      <button onClick={() => handleClick('outpaint')}>Outpaint</button>
    </div>
  );
};

export default ImageEditor;
