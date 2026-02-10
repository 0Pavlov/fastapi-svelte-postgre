# If for any reason the frontend is refusing to boot

You can setup it manually:
-Remove the whole frontend `rm -rf frontend`
-From this folder run `npx sv create frontend`
1. For the template pick SvelteKit minimal
2. For the type checking pick TypeScript syntax
3. Add tailwindcss
4. No typography or forms
5. npm package manager

Cd to the frontend folder `cd frontend`
run `npm install`

# Components
-Initialize shadcn-svelte to be able to use shadcn components `npx shadcn-svelte@latest init`
1. Pick the color scheme for the themes (I like Zinc or Neutral)
2. On every other option just press enter
-Install the components that are used in this project `npx shadcn-svelte@latest add button card spinner`
-Install mode-watcher for the theme-switcher button used in this project to work `npm i mode-watcher`
-Also if for some reason npm didn't optimized it itself, you need to make sure you have `@lucide/svelte` `npm install lucide-svelte`

# Files
-Now you just need to import the .svelte files from the repo `frontend/src/routes`
1. Copy the `+page.svelte` file to the folder
2. Copy the `AddTodoCard.svelte` component to the folder

# Run
run `npm run dev`
