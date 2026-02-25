# ПоДія — To-Do List PWA

A minimal, dependency-free to-do list app with offline support, installable as a
Progressive Web App (PWA) on Android Chrome and other modern browsers.

## Features

- ✅ Add, edit, complete, and delete tasks
- 💾 Tasks persisted to `localStorage` with versioned key `todo_v1` (migration-safe schema)
- 📦 Export / Import tasks as JSON
- 📶 Works offline after first load (service worker caches the app shell)
- 📲 Installable on Android Chrome and other PWA-capable browsers

## Local Development

No build step is required — the app is a single HTML file with inline CSS and JS.

### Serve locally

Use any static file server. Examples:

```bash
# Python (built-in)
python3 -m http.server 8080 --directory public/

# Node.js (npx)
npx serve public/
```

Then open <http://localhost:8080> in your browser.

> **Important:** The Service Worker only registers over `https://` or `http://localhost`.
> Always use `localhost` (not `127.0.0.1`) when testing locally.

## File Structure

```
public/
├── index.html        # Single-page app (all-inline, no dependencies)
├── manifest.json     # Web App Manifest
├── sw.js             # Service Worker (offline shell caching)
└── icons/
    ├── icon-192.png  # App icon 192 × 192
    └── icon-512.png  # App icon 512 × 512
```

## Data Schema

Tasks are stored in `localStorage` under the key **`todo_v1`**:

```json
{
  "version": 1,
  "tasks": [
    {
      "id": "<uuid>",
      "text": "Task description",
      "done": false,
      "createdAt": 1700000000000
    }
  ]
}
```

The loader is migration-safe: if it finds a plain array (legacy v0 format) it
automatically upgrades it to the current schema.

## Export / Import JSON

Click **⇅ JSON** in the header to open the panel:

- **⬇ Export JSON** — downloads all tasks as a `.json` file.
- **⬆ Import JSON** — imports tasks from a previously exported file; duplicates
  (matching `id`) are skipped so merging is safe.

## PWA Install (Android Chrome)

1. Open the app URL in Chrome on Android.
2. After a few seconds, Chrome shows an **"Add to Home screen"** banner  
   — or tap the **📲 Install** button in the app header.
3. Tap **Install** / **Add** to place the app icon on your home screen.
4. The app opens in **standalone** mode (no browser chrome) and works offline.

> On iOS Safari: tap the Share button → **Add to Home Screen**.

## Offline Behaviour

On first load the service worker (`sw.js`) caches the app shell
(`index.html`, `manifest.json`, icons).  
On subsequent loads — even without network — the app loads instantly from cache.

## Lighthouse PWA Checklist

The app is designed to pass the Lighthouse PWA audit:

| Check | Status |
|-------|--------|
| Has a web app manifest | ✅ `manifest.json` with required fields |
| Manifest has icons ≥ 192 px | ✅ `icon-192.png`, `icon-512.png` |
| `display: standalone` | ✅ |
| Service worker registered | ✅ `sw.js` |
| App shell cached offline | ✅ install event pre-caches shell URLs |
| HTTPS (or localhost) | ✅ required by browser for SW |
