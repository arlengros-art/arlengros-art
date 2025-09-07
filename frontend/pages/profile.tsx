import { useState } from "react";

export default function Profile() {
  const [apiKey, setApiKey] = useState<string | null>(null);

  const request = async (action: "create" | "delete") => {
    const res = await fetch("/api-keys", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer secret",
      },
      body: JSON.stringify({ action }),
    });
    return res.json();
  };

  const handleCreate = async () => {
    const data = await request("create");
    setApiKey(data.key);
  };

  const handleDelete = async () => {
    await request("delete");
    setApiKey(null);
  };

  return (
    <div>
      <h1>API Keys</h1>
      {apiKey && <p>Your key: {apiKey}</p>}
      <button onClick={handleCreate}>Создать</button>
      <button onClick={handleDelete}>Удалить</button>
    </div>
  );
}
