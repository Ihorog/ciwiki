# GitHub Pages Setup Instructions

## Quick Start

This repository is configured for automatic deployment to GitHub Pages using MkDocs. The site builds and deploys automatically on every push to `main`.

### ✅ What's Already Configured

1. **Workflow**: `.github/workflows/ciwiki-pages.yml` - Builds and deploys automatically
2. **Branch**: `gh-pages` - Auto-updated with built site
3. **Custom Domain**: `www.cimeika.com.ua` (configured via CNAME file)
4. **Build System**: MkDocs with Material theme

### ⚙️ Required Manual Configuration (One-Time Setup)

You need to configure GitHub Pages in the repository settings:

#### Step 1: Access Repository Settings

1. Go to https://github.com/Ihorog/ciwiki
2. Click on **Settings** tab
3. In the left sidebar, click **Pages** (under "Code and automation")

#### Step 2: Configure Source

In the **"Build and deployment"** section:

1. **Source**: Select **"Deploy from a branch"**
2. **Branch**: 
   - Select: `gh-pages`
   - Folder: `/ (root)`
3. Click **Save**

#### Step 3: Configure Custom Domain (if using)

In the **"Custom domain"** section:

1. Enter: `www.cimeika.com.ua`
2. Click **Save**
3. Wait for DNS check to complete
4. Enable **"Enforce HTTPS"** once DNS verification succeeds

#### Step 4: Verify

After configuration, you should see:

```
✅ Your site is live at https://www.cimeika.com.ua
```

Or without custom domain:

```
✅ Your site is live at https://ihorog.github.io/ciwiki/
```

## How It Works

```
┌─────────────┐
│  Push code  │
│  to main    │
└──────┬──────┘
       │
       v
┌─────────────────┐
│ GitHub Actions  │
│ runs workflow   │
└──────┬──────────┘
       │
       v
┌─────────────────┐
│ MkDocs builds   │
│ static site     │
└──────┬──────────┘
       │
       v
┌─────────────────┐
│ Deploy to       │
│ gh-pages branch │
└──────┬──────────┘
       │
       v
┌─────────────────┐
│ GitHub Pages    │
│ publishes site  │
└─────────────────┘
```

## Verification Steps

### 1. Check Workflow Status

- Go to: https://github.com/Ihorog/ciwiki/actions
- Find latest **"Build & Deploy CiWiki"** run
- Status should be ✅ (green checkmark)

### 2. Check gh-pages Branch

- Go to: https://github.com/Ihorog/ciwiki/tree/gh-pages
- Verify:
  - `index.html` exists
  - `.nojekyll` exists
  - Recent commit timestamp

### 3. Check Live Site

- Visit: https://www.cimeika.com.ua (or https://ihorog.github.io/ciwiki/)
- Verify content loads correctly
- Test navigation links

## Troubleshooting

### Site shows 404

**Causes:**
1. GitHub Pages not configured → Follow setup steps above
2. `gh-pages` branch empty → Trigger workflow manually
3. DNS not configured → Check domain DNS settings

### Site not updating

**Solutions:**
1. Check if workflow ran: Actions → Build & Deploy CiWiki
2. Clear browser cache: Ctrl+Shift+R (Cmd+Shift+R on Mac)
3. Wait 2-3 minutes for GitHub Pages to refresh

### Workflow failing

**Common issues:**
1. Missing files → Check workflow logs
2. MkDocs build errors → Test locally with `mkdocs build --strict`
3. Permission errors → Settings → Actions → Enable read/write permissions

## Local Development

To preview the site locally before pushing:

```bash
# Install dependencies
pip install mkdocs mkdocs-material

# Start dev server
mkdocs serve

# Open http://127.0.0.1:8000
```

## File Structure

### Source Files
```
docs/
├── index.md              # Homepage
├── processes/            # Process documentation
├── Legend-ci/           # Legend Ci docs
└── Cimeika/             # Project docs

mkdocs.yml               # MkDocs configuration
CNAME                    # Custom domain
```

### Built Site (gh-pages branch)
```
gh-pages/
├── index.html           # Built homepage
├── .nojekyll           # Disable Jekyll
├── assets/             # CSS, JS, images
└── ...                 # Other generated files
```

## Additional Resources

- **Full Documentation**: [docs/GITHUB_PAGES_SETUP.md](./docs/GITHUB_PAGES_SETUP.md) (Ukrainian)
- **Web Publishing Process**: [docs/processes/web-publishing.md](./docs/processes/web-publishing.md)
- **Workflow File**: [.github/workflows/ciwiki-pages.yml](./.github/workflows/ciwiki-pages.yml)
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **MkDocs**: https://www.mkdocs.org/
- **Material for MkDocs**: https://squidfunk.github.io/mkdocs-material/

## Status

**Last Updated**: 2026-01-25  
**Status**: ✅ Active and working  
**Latest Build**: Check [Actions](https://github.com/Ihorog/ciwiki/actions)

---

**Need Help?**
- Check workflow logs: [Actions](https://github.com/Ihorog/ciwiki/actions)
- Review [troubleshooting guide](./docs/GITHUB_PAGES_SETUP.md#troubleshooting)
- Create an issue with details
