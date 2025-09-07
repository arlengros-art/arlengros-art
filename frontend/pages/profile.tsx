import { useState, useEffect } from 'react';

interface Profile {
  username: string;
  bio: string;
  avatar_url: string;
  likes: number;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile>({
    username: '',
    bio: '',
    avatar_url: '',
    likes: 0,
  });

  useEffect(() => {
    if (profile.username) {
      fetch(`/profile/${profile.username}`)
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => data && setProfile(data));
    }
  }, [profile.username]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile),
    });
    if (res.ok) {
      setProfile(await res.json());
    }
  };

  return (
    <div>
      <h1>Profile</h1>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Username"
          value={profile.username}
          onChange={(e) => setProfile({ ...profile, username: e.target.value })}
        />
        <textarea
          placeholder="Bio"
          value={profile.bio}
          onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
        />
        <input
          placeholder="Avatar URL"
          value={profile.avatar_url}
          onChange={(e) => setProfile({ ...profile, avatar_url: e.target.value })}
        />
        <button type="submit">Save</button>
      </form>
      <div>
        <p>Likes: {profile.likes}</p>
      </div>
    </div>
  );
}
