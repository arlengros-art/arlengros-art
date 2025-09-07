import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { name, email, message } = req.body as {
    name?: string;
    email?: string;
    message?: string;
  };

  if (!name || !email || !message) {
    res.status(400).json({ error: 'Missing fields' });
    return;
  }

  // In a real application you could save to a database or send an email
  console.log('Feedback received:', { name, email, message });

  res.status(200).json({ ok: true });
}
