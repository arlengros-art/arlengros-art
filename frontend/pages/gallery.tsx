import { useState } from "react";

interface ImageItem {
  id: number;
  path: string;
  tags: string[];
}

export default function Gallery() {
  const [tags, setTags] = useState("");
  const [query, setQuery] = useState("");
  const [images, setImages] = useState<ImageItem[]>([]);

  const load = async () => {
    const params = new URLSearchParams();
    if (tags) params.append("tags", tags);
    if (query) params.append("q", query);
    const res = await fetch(`/gallery?${params.toString()}`);
    const data = await res.json();
    setImages(data);
  };

  return (
    <div>
      <input
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        placeholder="tags"
      />
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="search by meaning"
      />
      <button onClick={load}>Search</button>
      <div>
        {images.map((img) => (
          <div key={img.id}>
            <img src={img.path} alt="" />
            <div>{img.tags.join(", ")}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
