import { useState } from 'react';
import ImageEditor from '../components/ImageEditor';

const EditPage = () => {
  const [image, setImage] = useState<string>('');
  const [result, setResult] = useState<string>('');

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImage(reader.result as string);
    reader.readAsDataURL(file);
  };

  const sendEdit = async (
    imgBlob: Blob,
    maskBlob: Blob,
    prompt: string,
    mode: 'inpaint' | 'outpaint'
  ) => {
    const form = new FormData();
    form.append('image', imgBlob, 'image.png');
    form.append('mask', maskBlob, 'mask.png');
    form.append('prompt', prompt);
    form.append('mode', mode);
    const resp = await fetch('http://localhost:8000/edit', {
      method: 'POST',
      body: form,
    });
    const data = await resp.json();
    setResult(`data:image/png;base64,${data.image}`);
  };

  return (
    <div>
      <input type="file" onChange={handleFile} />
      {image && <ImageEditor src={image} onSubmit={sendEdit} />}
      {result && <img src={result} alt="result" />}
    </div>
  );
};

export default EditPage;
