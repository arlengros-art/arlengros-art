import { useState } from 'react';

interface Image {
  id: number;
  url: string;
  likes: number;
}

const initialImages: Image[] = [
  { id: 1, url: '/images/1.jpg', likes: 0 },
  { id: 2, url: '/images/2.jpg', likes: 0 },
  { id: 3, url: '/images/3.jpg', likes: 0 },
];

export default function GalleryPage() {
  const [images, setImages] = useState<Image[]>(initialImages);
  const [username, setUsername] = useState('');

  const like = async (id: number) => {
    const res = await fetch(`/like/${id}?username=${username}`, { method: 'POST' });
    if (res.ok) {
      const data = await res.json();
      setImages((imgs) =>
        imgs.map((img) => (img.id === id ? { ...img, likes: data.likes } : img))
      );
    }
  };

  return (
    <div>
      <h1>Gallery</h1>
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      {images.map((img) => (
        <div key={img.id}>
          <img src={img.url} alt="" />
          <span>{img.likes} likes</span>
          <button onClick={() => like(img.id)}>Like</button>
        </div>
      ))}
    </div>
  );
}
