# If for any reason the frontend is refusing to boot

You can setup it manually.

1. Remove the whole frontend:
   ```bash
   rm -rf frontend
   ```

2. From this folder run:
   ```bash
   npx sv create frontend
   ```
   * **Template:** SvelteKit minimal
   * **Type checking:** TypeScript syntax
   * **Add:** tailwindcss
   * **Options:** No typography or forms
   * **Package manager:** npm

3. CD to the frontend folder and install dependencies:
   ```bash
   cd frontend
   ```
   ```bash
   npm install
   ```

## Components

1. Initialize `shadcn-svelte` to be able to use shadcn components:
   ```bash
   npx shadcn-svelte@latest init
   ```
   * Pick the color scheme for the themes (I like Zinc or Neutral).
   * On every other option just press **Enter**.

2. Install the components that are used in this project:
   ```bash
   npx shadcn-svelte@latest add button card spinner
   ```

3. Install `mode-watcher` for the theme-switcher button used in this project to work:
   ```bash
   npm i mode-watcher
   ```

4. Also, if for some reason npm didn't optimize it itself, you need to make sure you have `@lucide/svelte`:
   ```bash
   npm install lucide-svelte
   ```

## Files

Now you just need to import the `.svelte` files from the repo `frontend/src/routes`:

1. Copy the `+page.svelte` file to the folder.
2. Copy the `AddTodoCard.svelte` component to the folder.

## Run

Run the development server:
```bash
npm run dev
```

Or to be accessible on a local network:
```bash
# Also don't forget to change the `localhost` in the +page.svelte file to the
# ip of the machine which runs the backend
npm run dev -- --host
```
