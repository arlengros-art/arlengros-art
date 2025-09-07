import React, { useEffect, useState } from 'react';
import ImageCard from '../components/ImageCard';

const GalleryPage: React.FC = () => {
  const [images, setImages] = useState<string[]>([]);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem('images') || '[]');
    setImages(stored);
  }, []);

  return (
    <div>
      {images.map((src, idx) => (
        <ImageCard key={idx} src={src} />
      ))}
    </div>
  );
};

export default GalleryPage;
