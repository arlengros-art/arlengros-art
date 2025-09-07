import React, { useState } from 'react';
import RequestForm from '../components/RequestForm';
import ImageCard from '../components/ImageCard';

const GeneratePage: React.FC = () => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleGenerate = async (prompt: string) => {
    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      if (data.url) {
        setImageUrl(data.url);
        const stored = JSON.parse(localStorage.getItem('images') || '[]');
        localStorage.setItem('images', JSON.stringify([data.url, ...stored]));
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div>
      <RequestForm onSubmit={handleGenerate} />
      {imageUrl && <ImageCard src={imageUrl} />}
    </div>
  );
};

export default GeneratePage;
