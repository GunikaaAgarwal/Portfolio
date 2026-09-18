# Gunikaa Agarwal — Portfolio

Complete export of the portfolio as of September 18, 2026. Includes all 15 case studies, project images, latest resume, filters, image zoom, magazine readers, photo stack, cursor effects, and hover/entrance animations.

## Publish using GitHub Pages

1. Create a new **public** GitHub repository named `gunikaa-portfolio`. Use the default `main` branch.
2. Extract this ZIP. Add its contents to the repository root: `build.py`, `content/`, `dist/`, and `.github/workflows/deploy.yml`. Do not upload the ZIP itself or add an extra enclosing folder. GitHub Desktop can copy and commit the whole extracted folder, including the workflow.
3. In the repository, open **Settings → Pages**. Under **Build and deployment → Source**, choose **GitHub Actions**.
4. Open **Actions → Publish portfolio → Run workflow**, choose `main`, then run it. If an earlier run failed before Pages was enabled, rerun it now.
5. Once the workflow succeeds, Settings → Pages displays your URL, usually `https://YOUR-USERNAME.github.io/gunikaa-portfolio/`.

Every later push to `main` rebuilds and publishes the site. No API keys, paid packages, Node installation, or custom backend are required. The workflow uses GitHub's built-in deployment identity.

Official setup reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Publish using Vercel

1. Import this repository into Vercel.
2. Set the build command to `python3 build.py`.
3. Set the output directory to `dist`.
4. Deploy the project. Vercel will publish the generated static site.

The root [`vercel.json`](vercel.json) already tells Vercel to build with `build.py` and serve `dist/`, so the deployment should work with the default project settings.

## Preview on your computer

With Python 3 installed, open a terminal in this folder:

```sh
python3 build.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. On Windows, use `py` if `python3` is unavailable. Press Ctrl+C to stop the server.

## Edit the portfolio

- `content/about.html`: About bio and photos.
- `content/profile.json`: experience, education, certifications, skills, tools.
- `content/existing-projects.json`: ABPAL, TAC, Rajasthan, Khushi case studies.
- `content/new-projects.json`: remaining project metadata and general case studies.
- `content/lissitzky.html` and `content/abpal-catalog.html`: custom editorial case studies.
- `content/galleries.json`: case-study galleries.
- `build.py`: homepage text, navigation, project ordering, shared page templates.
- `dist/style.css`: styles and CSS animations.
- `dist/interactions.js`: filters, readers, image zoom, and other interactions.
- `dist/assets/`: project images and downloadable resume (`gunikaa-resume.pdf`).

Edit `content/site-content.md`, the content JSON files, or `build.py`, then run `python3 build.py`. Generated `dist/*.html` pages will be replaced by that command, so edit their source templates rather than those generated pages. Keep `dist/style.css`, `dist/interactions.js`, and `dist/assets/` committed: they are source assets, not disposable build output.

`content/site-content.md` is the main source of truth for the homepage copy, navigation, contact details, and project ordering. Use that file when changing text like the hero sentence, instead of editing the generator.

When replacing the resume, replace `dist/assets/gunikaa-resume.pdf` and update its date query in `build.py` so returning visitors receive the new copy.

## Custom domain or other hosting

For GitHub Pages, add a domain you own in **Settings → Pages → Custom domain**, follow GitHub's verification and DNS instructions, and enable HTTPS when available. With this Actions workflow, the Pages settings are the authority for your domain.

Official domain guide: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

For another static host, publish the **contents of `dist/`**, or configure the build command as `python3 build.py` and output directory as `dist`. Relative internal links support both a domain root and a GitHub repository subpath.

This is an independent copy. Edits made later in the original hosted portfolio will not automatically sync to this GitHub repository, and edits here will not change the original site. Email links open the visitor's email application; the copy-email control works on HTTPS or localhost. Fonts and external project links still require an internet connection.

## Rights

Your portfolio content and supplied artwork retain their existing ownership. Historical artwork and third-party brand material remain subject to their respective rights. No open-source license is granted by this export.
