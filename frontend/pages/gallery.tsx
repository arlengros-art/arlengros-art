import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Gallery() {
  const router = useRouter();
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.replace('/login');
    }
  }, []);

  return <div>Gallery page</div>;
}
