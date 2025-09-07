import React, { useState } from 'react';

interface RequestFormProps {
  onSubmit: (prompt: string) => void;
}

const RequestForm: React.FC<RequestFormProps> = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(prompt);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Введите текст"
      />
      <button type="submit">Создать</button>
    </form>
  );
};

export default RequestForm;
