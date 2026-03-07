# Bala Subramanyam Sivarathri — Academic Portfolio

Live site hosted via **GitHub Pages**: `https://<your-username>.github.io/<repo-name>/`

## Files

| File | Purpose |
|------|---------|
| `index.html` | Main portfolio page |
| `style_msu.css` | MSU-branded stylesheet |
| `profile.jpg` | Hero headshot *(add your own)* |
| `greenhouse.jpg` | About section photo *(add your own)* |
| `field.jpg` | Skills section photo *(add your own)* |
| `presentation.jpg` | Research section photo *(add your own)* |
| `awards.jpg` | Achievements section photo *(add your own)* |

## How to Publish on GitHub Pages

1. **Create a new repository** on GitHub (e.g. `bala-portfolio`). Make it **Public**.
2. **Upload all files** — drag and drop into the repo, or use Git:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio"
   git branch -M main
   git remote add origin https://github.com/<your-username>/bala-portfolio.git
   git push -u origin main
   ```
3. Go to **Settings → Pages** in your repo.
4. Under **Source**, select **Deploy from a branch → main → / (root)**.
5. Click **Save**. Your site will be live in ~1 minute at:
   `https://<your-username>.github.io/bala-portfolio/`

## Adding Your Photos

Place these image files in the **root of the repo** (same folder as `index.html`):

- `profile.jpg` — your headshot (recommended ~500×500px)
- `greenhouse.jpg` — greenhouse photo (~400×400px)
- `field.jpg` — field photo (~400×500px, portrait)
- `presentation.jpg` — presentation photo (~800×450px, landscape)
- `awards.jpg` — awards photo (~800×450px, landscape)

## Contact Form

The contact form uses a **mailto:** link. When a visitor submits the form, their default email client will open with a pre-filled message to `bs2437@msstate.edu`. No backend or third-party service required.

For a fully functional hosted form, consider [Formspree](https://formspree.io) (free tier available) — replace the `<form>` action with your Formspree endpoint.
