import type { AppProps } from 'next/app';
import MainMenu from '../components/MainMenu';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <MainMenu />
      <Component {...pageProps} />
    </>
  );
}
