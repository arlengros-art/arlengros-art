import posthog from 'posthog-js';

const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;

if (typeof window !== 'undefined' && key) {
  posthog.init(key, { api_host: 'https://app.posthog.com' });
}

export const trackPageView = (url: string): void => {
  if (!key) return;
  posthog.capture('$pageview', { url });
};

export const trackGeneration = (id: string): void => {
  if (!key) return;
  posthog.capture('generation', { id });
};
