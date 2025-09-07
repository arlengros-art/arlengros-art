import { useEffect, useState } from "react";

export function useNotifications(enabled: boolean) {
  const [subscription, setSubscription] = useState<PushSubscription | null>(null);

  useEffect(() => {
    if (!enabled) {
      return;
    }
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
      return;
    }

    async function register() {
      const reg = await navigator.serviceWorker.register("/sw.js");
      let sub = await reg.pushManager.getSubscription();
      if (!sub) {
        sub = await reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: "PUBLIC_KEY_PLACEHOLDER",
        });
      }
      setSubscription(sub);
      // TODO: send subscription to backend for storage
    }

    register();
  }, [enabled]);

  return subscription;
}
