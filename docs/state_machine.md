# State Machines

The **server is authoritative**. Clients render state; they never decide scores, winners, turn order, words, timers, or document validity.

---

## Room states

```
OPEN → LOBBY → PLAYING → GAME_FINISHED → IDLE → DESTROYED
```

| State | Description |
|-------|-------------|
| `OPEN` | Room created, waiting for players |
| `LOBBY` | Pre-game lobby; ready toggles, host can start |
| `PLAYING` | Active game in progress |
| `GAME_FINISHED` | Final scores shown; optional gallery publish |
| `IDLE` | Post-game idle; eligible for cleanup |
| `DESTROYED` | Room removed from memory |

### Room rules

- Join allowed in `OPEN`, `LOBBY`, or `PLAYING` (reconnect).
- Join rejected in `IDLE` → `ROOM_FULL`.
- Max **10 active players**; overflow becomes `SPECTATING`.
- Host transfers on host leave to next active player.
- Idle cleanup: `OPEN` / `LOBBY` / `IDLE` rooms auto-delete after inactivity timeout.

---

## Game states

```
LOBBY → WORD_SELECTION → ROUND_COUNTDOWN → DRAWING
  → ROUND_REVEAL → SCOREBOARD → NEXT_ROUND → … → GAME_FINISHED
```

| State | Description |
|-------|-------------|
| `LOBBY` | Game object exists but round not started |
| `WORD_SELECTION` | Drawer picks from 3 word choices |
| `ROUND_COUNTDOWN` | Brief countdown before drawing |
| `DRAWING` | Active round timer; guesses accepted |
| `DRAWER_DISCONNECTED` | Drawer offline; timer paused |
| `ROUND_REVEAL` | Word revealed, scores updated |
| `SCOREBOARD` | Between-round delay |
| `NEXT_ROUND` | Preparing next drawer |
| `GAME_FINISHED` | All rounds complete |

### Round flow

1. After `game.started`, auto-begin first round.
2. Pick drawer (rotate through active players).
3. Emit `round.starting` with 3 word choices.
4. Drawer selects via `word.select`, or auto-pick after **10s** timeout.
5. Drawer → `DRAWING`; others → `GUESSING`.
6. Round timer runs (default **60s**); emit `timer.tick` / `timer.warning`.
7. On correct guess or timeout → `round.revealed` → `SCOREBOARD` → next round or `GAME_FINISHED`.

### Drawer disconnect

During `DRAWING`:

1. Transition to `DRAWER_DISCONNECTED`.
2. Pause round timer.
3. Start **20s** grace timer (configurable).
4. On reconnect within grace → resume `DRAWING`, emit `player.reconnected`.
5. On timeout → skip turn, advance round.

### Non-drawer disconnect

During `PLAYING`:

- Preserve player state (`GUESSING`, `SOLVED`, `WAITING`, `SPECTATING`).
- Reject guesses, chat, and shape ops while disconnected.
- On reconnect → restore state, emit `player.reconnected`.
- After grace timeout (**~2–5 min**) → promote to spectator (`player.becameSpectator`).
- Disconnected players remain in drawer rotation per domain rules.

### Game end

- After `GAME_FINISHED`, room returns to `LOBBY` for rematch.
- Spectators may rejoin active rotation (respect max 10 players).

---

## Player states

| State | When |
|-------|------|
| `CONNECTED` | In room, not ready |
| `READY` | Ready in lobby |
| `DRAWING` | Current drawer |
| `GUESSING` | Active guesser during round |
| `SOLVED` | Correctly guessed this round |
| `WAITING` | Waiting for turn |
| `SPECTATING` | Overflow or demoted after disconnect |
| `DISCONNECTED` | Connection lost |
| `RECONNECTED` | Transient flag on reconnect |

---

## Drawer connection state

Separate from player state during drawing:

| State | Meaning |
|-------|---------|
| `CONNECTED` | Drawer online |
| `DISCONNECTED` | Drawer offline, grace running |
| `RECONNECTED` | Drawer returned within grace |
