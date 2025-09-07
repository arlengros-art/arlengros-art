import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { name, email, message } = req.body;
    console.log('Feedback received:', { name, email, message });
    res.status(200).json({ ok: true });
  } else {
    res.status(405).end();
  }
}
