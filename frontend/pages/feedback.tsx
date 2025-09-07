import React, { useState } from 'react';

export default function FeedbackPage() {
  const [status, setStatus] = useState<string>('');

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const body = {
      name: formData.get('name'),
      email: formData.get('email'),
      message: formData.get('message'),
    };

    const response = await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (response.ok) {
      setStatus('Спасибо за ваш фидбэк!');
      form.reset();
    } else {
      setStatus('Ошибка отправки. Попробуйте позже.');
    }
  }

  return (
    <main>
      <h1>Отправьте нам свой фидбэк</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Имя
          <input type="text" name="name" required />
        </label>
        <label>
          Email
          <input type="email" name="email" required />
        </label>
        <label>
          Сообщение
          <textarea name="message" required />
        </label>
        <button type="submit">Отправить</button>
      </form>
      {status && <p>{status}</p>}
    </main>
  );
}
