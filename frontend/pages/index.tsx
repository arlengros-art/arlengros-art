import {useTranslations} from 'next-intl';

export default function IndexPage() {
  const t = useTranslations('Index');
  return <h1>{t('greeting')}</h1>;
}

export async function getStaticProps({locale}: {locale: string}) {
  return {
    props: {
      messages: (await import(`../locales/${locale}.json`)).default
    }
  };
}
