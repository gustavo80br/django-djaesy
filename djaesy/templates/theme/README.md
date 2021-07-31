[![Netlify Status](https://api.netlify.com/api/v1/badges/2bd72e04-e087-4f19-b3b4-2fd3fa1f58a6/deploy-status)](https://app.netlify.com/sites/b7-time-tracker/deploys)
# b7_frontend
Frontend Vuejs project for B7 Time Tracker Prototype

## Element components

See [Element Library Documentation](https://element-plus.org/#/en-US )

We are using on-demand components installation, so in order to use a component, add the `import` and the `Vue.use` lines in `plugins/element.js` file.

## Tailwindcss

See [Tailwindcss Documentation](https://tailwindcss.com/docs)

We are using this utility class css library. If you have never worked with tailwindcss before... give it a shot!

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run dev
```

### Compiles and minifies for production
```
npm run build
```

## Contributing
Developer workflow:
- Create branch from `main`
- Work in branch, commit changes.
- Rebase with `main` before pushing if necessary
- Push to github
- Create Pull Request to `main`, assign some reviewer.
- When creating a PR, Netlify will create a preview URL and add some details to the PR if you want to test life your changes before PR is merged.

