# WebSocket Event Protocol

Svigl uses a **single WebSocket connection per client**.

Every message has exactly this shape:

```json
{ "type": "<event_name>", "payload": { ... } }
```

## Naming convention

| Direction | Style | Example |
|-----------|-------|---------|
| Client → Server | Imperative | `shape.commit` |
| Server → Client | Past tense | `shape.committed` |

This keeps frontend and backend compatible.

---

## Client → Server events

| Event | Payload | Description |
|-------|---------|-------------|
| `room.join` | `{ roomCode, displayName?, authToken? }` | Join or reconnect to a room |
| `room.leave` | `{}` | Leave the room |
| `player.ready` | `{}` | Toggle ready state in lobby |
| `game.start` | `{}` | Host starts the game |
| `word.select` | `{ wordIndex: number }` | Drawer picks a word |
| `shape.preview` | `{ shapeId, preview }` | Ephemeral in-progress shape |
| `shape.commit` | `{ shape }` | Commit a shape to the document |
| `shape.update` | `{ shapeId, changes }` | Update an existing shape |
| `shape.undo` | `{ operationId }` | Undo last committed operation |
| `guess.submit` | `{ guess: string }` | Submit a guess |
| `chat.message` | `{ message: string }` | Drawer chat or free chat |
| `gallery.publish` | `{ publish: boolean }` | Publish final drawing |
| `vote.submit` | `{ drawingId, vote: "up" \| "down" }` | Vote on gallery post |
| `connection.ping` | `{ ts: number }` | Heartbeat |

---

## Server → Client events

### Room lifecycle

| Event | Payload |
|-------|---------|
| `room.joined` | `{ room, selfId }` |
| `room.updated` | `{ room }` |
| `player.joined` | `{ player }` |
| `player.left` | `{ playerId }` |
| `player.disconnected` | `{ playerId }` |
| `player.reconnected` | `{ playerId, state? }` |
| `player.ready` | `{ playerId, ready }` |
| `player.becameDrawer` | `{ playerId }` |
| `player.becameSpectator` | `{ playerId }` |

### Game / rounds

| Event | Payload |
|-------|---------|
| `game.started` | `{ game }` |
| `round.starting` | `{ round, drawerId, wordChoices? }` |
| `round.started` | `{ round, wordHints }` |
| `round.finished` | `{ round }` |
| `round.revealed` | `{ round, word }` |

### Drawing

| Event | Payload |
|-------|---------|
| `shape.previewed` | `{ shapeId, preview }` |
| `shape.committed` | `{ shape, operationId }` |
| `shape.updated` | `{ shapeId, changes, operationId }` |
| `shape.undone` | `{ operationId }` |

### Guesses / chat

| Event | Payload |
|-------|---------|
| `guess.correct` | `{ playerId }` |
| `guess.close` | `{ playerId }` |
| `guess.incorrect` | `{ playerId }` |
| `chat.message` | `ChatMessage` |

### Timer / score

| Event | Payload |
|-------|---------|
| `timer.tick` | `{ remaining }` |
| `timer.warning` | `{ remaining }` |
| `timer.finished` | `{}` |
| `score.updated` | `{ playerId, score }` |
| `leaderboard.updated` | `{ scores }` |

### Gallery

| Event | Payload |
|-------|---------|
| `gallery.published` | `{ drawingId }` |
| `vote.recorded` | `{ drawingId }` |

### Connection / errors

| Event | Payload |
|-------|---------|
| `connection.pong` | `{ ts }` |
| `error` | `{ code, message }` |

---

## Error codes

| Code | Meaning |
|------|---------|
| `INVALID_STATE` | Action not allowed in current room/game state |
| `INVALID_SHAPE` | Shape failed validation |
| `INVALID_WORD` | Invalid word selection |
| `ROOM_FULL` | Room at capacity |
| `NOT_HOST` | Only the host may perform this action |
| `TIMEOUT` | Action timed out |
| `UNAUTHORIZED` | Auth required or token invalid |
| `UNKNOWN_EVENT` | Unrecognized event type |

---

## TypeScript mirror

When implementing the frontend backend integration, mirror this protocol in `svigl/types/events.ts` so client sends and server handlers stay aligned.
