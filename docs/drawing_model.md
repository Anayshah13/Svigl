# Drawing Model

Svigl does not support freehand raster drawing. Every drawing is composed of **SVG vector primitives**.

Supported shape types:

* Path (Bézier nodes with handles)
* Rectangle
* Circle

---

## Canvas

- ViewBox: **800 × 600**
- Coordinates are in SVG space, not screen pixels.
- The client converts pointer events to viewBox coordinates before sending shapes.

---

## Shape

Every shape shares:

```text
Shape
├── id
├── type             rectangle | circle | path
├── geometry         type-specific
├── style
├── createdBy        player id
├── createdAt
└── updatedAt
```

### Rectangle geometry

`{ x, y, width, height }`

### Circle geometry

`{ cx, cy, radius }`

### Path geometry

```text
PathGeometry
└── nodes[]
    ├── id
    ├── position       { x, y }
    ├── incomingHandle { x, y } | null
    └── outgoingHandle { x, y } | null
```

Paths are smoothed client-side before preview/commit.

---

## Style

```text
Style
├── strokeColor      palette color
├── strokeWidth      1 | 2 | 4 | 6 | 8 | 12
├── fillColor        color | "none"
└── opacity          0–1
```

---

## DrawingDocument

Instead of storing rendered SVG files, Svigl stores a sequence of operations.

```text
DrawingDocument
├── id
├── version          increments on each mutation
├── createdAt
├── operations[]     audit log
└── shapes[]         materialized shapes for render
```

Example operation history:

```text
Commit Rectangle
→ Commit Path
→ Resize Rectangle
→ Undo
→ Commit Circle
```

The SVG is generated from shapes whenever needed (live canvas, gallery replay).

---

## Operation types

| Type | Description |
|------|-------------|
| `shape.commit` | Add a new shape |
| `shape.update` | Modify an existing shape |
| `shape.undo` | Remove shape from last operation |

Each committed operation receives a server-assigned `operationId` used for undo.

---

## Client / server responsibilities

| Layer | Responsibility |
|-------|----------------|
| Client | Pointer tools, local previews, send intentions |
| Server | Validate shapes, assign operation IDs, broadcast commits |
| Renderer | **Only** component that emits SVG markup |

The renderer (`SvgRenderer`) is the single source of SVG output. No other component writes raw SVG strings.

---

## Preview vs commit

| Phase | Transport | Persisted? |
|-------|-----------|------------|
| Preview | `shape.preview` → `shape.previewed` | No — ephemeral |
| Commit | `shape.commit` → `shape.committed` | Yes — appended to document |

Previews are shown with dashed strokes during drag. Cleared on commit or cancel.

---

## Validation rules

The server rejects shapes that:

- Are below minimum size (accidental dots)
- Come from non-drawer clients
- Arrive outside `DRAWING` game state
- Exceed per-shape limits (path node count, etc.)

Invalid commits return `error` with code `INVALID_SHAPE`.

---

## Tools

| Tool | Key | Behavior |
|------|-----|----------|
| Pointer | V | Select (no drawing) |
| Path | P | Click-drag freeform path |
| Rectangle | R | Click-drag axis-aligned rect |
| Circle | O | Click-drag from center |

Undo removes the last committed operation from the document and broadcasts `shape.undone`.
