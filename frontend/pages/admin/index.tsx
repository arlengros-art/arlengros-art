import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

type Image = {
  id: number;
  url: string;
};

type User = {
  role: string;
};

export default function AdminPage() {
  const router = useRouter();
  const [images, setImages] = useState<Image[]>([]);

  useEffect(() => {
    // Check user role before displaying the page
    fetch('/api/me')
      .then((res) => res.json())
      .then((user: User) => {
        if (user.role !== 'admin') {
          router.replace('/');
          return;
        }
        loadImages();
      })
      .catch(() => router.replace('/'));
  }, []);

  const loadImages = () => {
    fetch('/admin/images')
      .then((res) => res.json())
      .then((data) => setImages(data));
  };

  const approve = (id: number) => {
    fetch(`/admin/image/${id}/approve`, { method: 'POST' }).then(loadImages);
  };

  const remove = (id: number) => {
    fetch(`/admin/image/${id}`, { method: 'DELETE' }).then(loadImages);
  };

  return (
    <div>
      <h1>Pending images</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {images.map((img) => (
            <tr key={img.id}>
              <td>{img.id}</td>
              <td>{img.url}</td>
              <td>
                <button onClick={() => approve(img.id)}>Approve</button>
                <button onClick={() => remove(img.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
