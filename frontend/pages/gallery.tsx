import { useEffect, useState } from 'react';

interface GalleryItem {
  id: number;
  path: string;
  prompt: string;
  created_at: string;
}

export default function Gallery() {
  const [items, setItems] = useState<GalleryItem[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/gallery')
      .then((res) => res.json())
      .then((data) => setItems(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
      {items.map((img) => (
        <div key={img.id}>
          <img src={`http://localhost:8000${img.path}`} alt={img.prompt} style={{ width: '100%' }} />
          <p>{img.prompt}</p>
        </div>
      ))}
    </div>
  );
}
