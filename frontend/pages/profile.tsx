import React, { useState } from "react";
import { useNotifications } from "../hooks/useNotifications";

export default function Profile() {
  const [enabled, setEnabled] = useState(false);
  const subscription = useNotifications(enabled);

  return (
    <div>
      <h1>Profile</h1>
      <label>
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => setEnabled(e.target.checked)}
        />
        Enable notifications
      </label>
      {subscription && <p>Notifications active</p>}
    </div>
  );
}
