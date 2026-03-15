# story.json Reference Guide

## File Location
`pygame/data/story.json`

---

## Top-Level Structure
```json
{
  "scenes": [ ...list of scene objects... ]
}
```

---

## Scene Object

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✅ | Unique identifier for the scene |
| `background` | string | ✅ | Background image filename from `assets/backgrounds/` |
| `characters` | array | ✅ | Initial characters shown at the start of the scene. Use `[]` for no characters |
| `dialogue` | array | ✅ | List of dialogue lines in order |

---

## Character Object

Used in both scene-level `characters` and per-dialogue `characters`.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Character name, also used to find the sprite file |
| `position` | string | ✅ | `"left"`, `"center"`, or `"right"` |
| `expression` | string | ✅ | Expression variant e.g. `"neutral"`, `"happy"`, `"surprised"` |
| `outfit` | string | ❌ | Outfit/costume variant e.g. `"spacesuit"`, `"casual"` |

**Sprite filename formula:**
```
# With outfit:
assets/characters/{name}_{outfit}_{expression}.png

# Without outfit (fallback):
assets/characters/{name}_{expression}.png

Examples:
  name="Lyra", outfit="spacesuit", expression="happy"
  → assets/characters/lyra_spacesuit_happy.png

  name="Lyra", expression="neutral" (no outfit)
  → assets/characters/lyra_neutral.png
```

**Position X coordinates:**
| Position | X value |
|---|---|
| `left` | 220 |
| `center` | 640 |
| `right` | 1060 |

---

## Dialogue Object

| Field | Type | Required | Description |
|---|---|---|---|
| `speaker` | string | ✅ | Name shown on the name plate. Use `""` for narration |
| `text` | string | ✅ | The dialogue text to display |
| `characters` | array | ❌ | Overrides which characters are on screen for this line only |

**Notes:**
- If a dialogue line has no `characters` field, the screen stays as-is from the previous line
- The scene-level `characters` field sets the initial state for the first line
- Setting `speaker` to `""` hides the name plate (use for narration or inner thoughts)
- Outfit can also be changed mid-scene by setting `outfit` on a per-dialogue `characters` entry
- To remove all characters from screen, pass an empty `characters: []` on a dialogue line

---

## Player Name

The player enters their name at the start of the game. You can use the `{player}` token
anywhere in `text` or `speaker` fields and it will be replaced with the actual player name at runtime.
```json
{ "speaker": "Lyra", "text": "So your name is {player}? Welcome aboard." }
{ "speaker": "{player}", "text": "I've always dreamed of reaching the stars." }
```

---

## Full Example
```json
{
  "scenes": [
    {
      "id": "opening_narration",
      "background": "deep_space.png",
      "characters": [],
      "dialogue": [
        {
          "speaker": "",
          "text": "The void stretched endlessly in every direction."
        },
        {
          "speaker": "",
          "text": "Somewhere out there, a lone ship drifted toward the unknown."
        }
      ]
    },
    {
      "id": "intro",
      "background": "space_station.png",
      "characters": [
        { "name": "Lyra", "position": "left", "expression": "neutral", "outfit": "spacesuit" }
      ],
      "dialogue": [
        {
          "speaker": "Lyra",
          "text": "So your name is {player}? Welcome aboard.",
          "characters": [
            { "name": "Lyra", "position": "left", "expression": "neutral", "outfit": "spacesuit" }
          ]
        },
        {
          "speaker": "Lyra",
          "text": "Wait... something is out there.",
          "characters": [
            { "name": "Lyra", "position": "left", "expression": "surprised", "outfit": "spacesuit" }
          ]
        },
        {
          "speaker": "",
          "text": "The stars stretched endlessly beyond the viewport."
        },
        {
          "speaker": "Lyra",
          "text": "We need to tell the crew.",
          "characters": [
            { "name": "Lyra", "position": "left", "expression": "serious", "outfit": "spacesuit" },
            { "name": "Rex", "position": "right", "expression": "neutral", "outfit": "casual" }
          ]
        }
      ]
    },
    {
      "id": "crew_quarters",
      "background": "crew_quarters.png",
      "characters": [
        { "name": "Lyra", "position": "center", "expression": "neutral", "outfit": "casual" }
      ],
      "dialogue": [
        {
          "speaker": "Lyra",
          "text": "Finally off duty. Time to rest.",
          "characters": [
            { "name": "Lyra", "position": "center", "expression": "neutral", "outfit": "casual" }
          ]
        }
      ]
    }
  ]
}
```

---

## Quick Tips

- Scene order in the `scenes` array is the play order
- Each scene's `id` is not used for navigation yet but keep it unique for future branching support
- You can show up to 3 characters at once (one per position)
- Placing a new character at a position that already has one will replace them
- Outfit can be changed mid-scene by updating the `outfit` field in a per-dialogue `characters` entry
- Use `characters: []` at scene level or on a dialogue line to show no characters at all
- If no `outfit` is specified the engine falls back to `{name}_{expression}.png`
- Use `{player}` anywhere in `text` or `speaker` to insert the player's chosen name