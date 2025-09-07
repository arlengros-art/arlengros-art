import { useState } from 'react';

export default function Feedback() {
  const [status, setStatus] = useState('');

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      email: (form.elements.namedItem('email') as HTMLInputElement).value,
      message: (form.elements.namedItem('message') as HTMLTextAreaElement).value,
    };

    const res = await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      setStatus('Спасибо за ваш отзыв!');
      form.reset();
    } else {
      setStatus('Ошибка отправки.');
    }
  }

  return (
    <div>
      <h1>Обратная связь</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Имя
            <input name="name" type="text" required />
          </label>
        </div>
        <div>
          <label>
            Email
            <input name="email" type="email" required />
          </label>
        </div>
        <div>
          <label>
            Сообщение
            <textarea name="message" required />
          </label>
        </div>
        <button type="submit">Отправить</button>
      </form>
      {status && <p>{status}</p>}
    </div>
  );
}
