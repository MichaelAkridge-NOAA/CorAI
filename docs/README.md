# CorAI Codelabs

This site hosts interactive tutorials for workspace tools and data annotation, using [Google Codelabs tools](https://github.com/googlecodelabs/tools).

## Tutorials
- [Install Label Studio with Docker](https://googlecodelabs.github.io/tools/codelab/static/?path=/workspaces/CorAI/codelabs/labelstudio-docker-install.md)

## How to Add a New Codelab
1. Write your tutorial in the `codelabs/` folder using the [Codelab Markdown format](https://github.com/googlecodelabs/tools/blob/master/FORMAT-GUIDE.md).
2. Push to `main`. The site will auto-build and deploy to GitHub Pages.
3. Add a link to your new codelab in `docs/index.html`.

## Local Development
Install the Codelabs tools:

```bash
npm install -g @googlecodelabs/tools
```

Preview a codelab locally:

```bash
claat serve codelabs/*.md
```

## Resources
- [Google Codelabs Tools](https://github.com/googlecodelabs/tools)
- [Label Studio](https://labelstud.io/)
