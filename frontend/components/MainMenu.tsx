import Link from 'next/link';

export default function MainMenu() {
  return (
    <nav>
      <ul>
        <li>
          <Link href="/">Главная</Link>
        </li>
        <li>
          <Link href="/feedback">Обратная связь</Link>
        </li>
      </ul>
    </nav>
  );
}
