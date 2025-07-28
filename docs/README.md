
# CorAI Codelabs

This site hosts interactive tutorials for workspace tools and data annotation, built with [Google Codelabs tools](https://github.com/googlecodelabs/tools).

## How it works
- All codelab source files are in the `codelabs/` folder (Markdown format).
- On every push to `main`, GitHub Actions builds the HTML and puts it in `docs/codelabs/`.
- The landing page is `docs/index.html`.
- GitHub Pages serves everything from the `docs/` folder.

## Add a new codelab
1. Write your tutorial in `codelabs/` using the [Codelab Markdown format](https://github.com/googlecodelabs/tools/blob/master/FORMAT-GUIDE.md).
2. Add a link to your new codelab in `docs/index.html` (link to the generated folder, e.g. `codelabs/your-codelab-id/`).
3. Commit and push to `main`. The site will auto-update.

## Local preview (optional)
If you want to preview locally:
1. Install Go (https://go.dev/doc/install)
2. Install claat:
   ```bash
   go install github.com/googlecodelabs/tools/claat@latest
   export PATH=$PATH:$(go env GOPATH)/bin
   ```
3. Run:
   ```bash
   claat serve codelabs/*.md
   ```

## Resources
- [Google Codelabs Tools](https://github.com/googlecodelabs/tools)
- [Label Studio](https://labelstud.io/)
