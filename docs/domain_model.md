# Domain Model

Core objects that exist inside Svigl during gameplay. The client receives a **read-only projection** of this model over WebSocket events.

Server-only fields (raw WebSocket handles, internal timers, connection maps) are never sent to clients.

---

## Player

```text
Player
├── id
├── displayName
├── avatar
├── isGuest
├── state          (PlayerState)
├── score
├── connected
├── joinedAt
└── guessedCorrectly
```

- Guests play without authentication.
- Authenticated users may link `authToken` on `room.join` for stats persistence.

---

## Room

```text
Room
├── id
├── code           (5-char share code)
├── hostId
├── state          (RoomState)
├── createdAt
├── lastActivity
├── players[]      (max 10 active)
├── spectators[]
├── game           (Game | null)
└── document       (DrawingDocument | null)
```

---

## Game

```text
Game
├── state          (GameState)
├── round
├── totalRounds    (default 3)
├── currentDrawerId
├── currentWord          (drawer only)
├── currentWordHints     (masked for guessers)
├── startedAt
├── remainingTime
├── drawerConnectionState
└── scores             (Scoreboard)
```

The server **never** sends `currentWord` to non-drawer clients. Guessers receive masked hints like `c _ _` instead.

---

## Scoreboard

```text
Scoreboard
└── playerScores[]  { playerId, score }
```

Updated on correct guesses and round end. Emitted via `leaderboard.updated`.

---

## ChatMessage

```text
ChatMessage
├── id
├── playerId       ("system" for server messages)
├── message
├── timestamp
└── kind           chat | guess | system | solved
```

The server tags `kind` so the UI knows how to render each line.

---

## GalleryEntry

Published drawing shown on the gallery page.

```text
GalleryEntry
├── id
├── authorId
├── authorName
├── roomId
├── roomCode
├── word
├── replay           (DrawingDocument)
├── upvotes
├── downvotes
└── publishedAt
```

Published by the final-round drawer via `gallery.publish` after `GAME_FINISHED`.

---

## Invariants

1. Only the drawer may commit shapes during `DRAWING`.
2. Only the host may send `game.start`.
3. Players who solved cannot guess again until next round.
4. Document operations are append-only except undo (pop last operation).
5. Live room state is **in-memory**; Postgres stores matches, gallery, and user stats only.
