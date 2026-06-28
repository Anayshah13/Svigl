# Database

Svigl uses **PostgreSQL** for persistence. In production this is typically **Supabase**; locally you can use Docker Postgres or SQLite for tests.

**Live room state is never stored in the database.** Only finished matches, gallery posts, votes, and user statistics are persisted.

---

## What is NOT stored

* Active room state
* In-progress game state
* WebSocket connections
* Ephemeral shape previews
* Current timer values

---

## Tables

### `users`

Google-authenticated accounts.

| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT PK | UUID |
| `username` | TEXT | Display name |
| `avatar_url` | TEXT | Optional |
| `provider` | TEXT | e.g. `google` |
| `created_at` | TIMESTAMPTZ | |

---

### `matches`

Finished game records.

| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT PK | Match UUID |
| `room_code` | TEXT | Share code |
| `started_at` | TIMESTAMPTZ | |
| `ended_at` | TIMESTAMPTZ | |
| `total_rounds` | INTEGER | |
| `winner_id` | TEXT | User id |
| `created_at` | TIMESTAMPTZ | |

---

### `match_players`

Per-player scores for a finished match.

| Column | Type | Notes |
|--------|------|-------|
| `match_id` | TEXT FK → matches | |
| `user_id` | TEXT | Registered user id |
| `final_score` | INTEGER | |
| `placement` | INTEGER | 1 = winner |

Primary key: `(match_id, user_id)`

---

### `player_statistics`

Aggregated stats for registered users.

| Column | Type | Default |
|--------|------|---------|
| `user_id` | TEXT PK FK → users | |
| `games_played` | INTEGER | 0 |
| `games_won` | INTEGER | 0 |
| `total_score` | INTEGER | 0 |
| `drawings_published` | INTEGER | 0 |
| `total_votes` | INTEGER | 0 |
| `created_at` | TIMESTAMPTZ | NOW() |
| `updated_at` | TIMESTAMPTZ | NOW() |

Guest players are not tracked in statistics.

---

### `gallery_posts`

Published drawings with replay data.

| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT PK | |
| `author_id` | TEXT | User or guest id |
| `match_id` | TEXT | Source match |
| `replay_data` | JSONB | Document envelope |
| `svg_snapshot` | TEXT | Optional rendered snapshot |
| `upvotes` | INTEGER | Denormalized count |
| `downvotes` | INTEGER | Denormalized count |
| `published_at` | TIMESTAMPTZ | |

#### Replay JSONB envelope

```json
{
  "v": 1,
  "roomCode": "ABCDE",
  "authorName": "Alice",
  "word": "umbrella",
  "document": { ... DrawingDocument ... }
}
```

---

### `votes`

One vote per user per gallery post.

| Column | Type | Notes |
|--------|------|-------|
| `user_id` | TEXT | |
| `gallery_post_id` | TEXT FK → gallery_posts | |
| `vote` | SMALLINT | `-1` or `1` |
| `created_at` | TIMESTAMPTZ | |

Primary key: `(user_id, gallery_post_id)`

---

## Migrations

Migrations are applied manually (no Alembic):

```bash
psql $DATABASE_URL -f backend/migrations/001_gallery_schema.sql
psql $DATABASE_URL -f backend/migrations/002_match_players_stats.sql
```

Use your Supabase pooler connection string for hosted Postgres.

---

## Repository pattern

| Feature | With DB | Without DB |
|---------|---------|------------|
| Gallery | `PostgresGalleryRepository` | `InMemoryGalleryRepository` |
| Matches | `PostgresMatchRepository` | `NoOpMatchRepository` |
| Auth users | `UserRepository` | JWT only, no persistence |

When implementing the backend, wire repositories in `app/create_app.py` based on `SVIGL_DATABASE_URL`.
