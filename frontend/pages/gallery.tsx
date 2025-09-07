import { useEffect, useState } from 'react';

interface GalleryItem {
  id: number;
  prompt: string;
  style: string;
}

const GalleryPage = () => {
  const [q, setQ] = useState('');
  const [style, setStyle] = useState('');
  const [items, setItems] = useState<GalleryItem[]>([]);

  const load = () => {
    const params = new URLSearchParams();
    if (q) params.append('q', q);
    if (style) params.append('style', style);
    fetch(`/gallery?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => setItems(data));
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select value={style} onChange={(e) => setStyle(e.target.value)}>
          <option value="">All styles</option>
          <option value="realistic">Realistic</option>
          <option value="abstract">Abstract</option>
        </select>
        <button onClick={load}>Apply</button>
      </div>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.prompt} ({item.style})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GalleryPage;
