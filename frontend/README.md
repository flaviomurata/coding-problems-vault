# Frontend

This package contains the React frontend for Coding Problems Vault.

## Requirements

- [Bun 1.4.0](https://bun.sh/)

## Install dependencies

Run this command from the repository root:

```sh
bun install
```

## Start the development server

Run this command from the repository root:

```sh
bun run dev
```

Vite serves the app at `http://localhost:5173` by default.

## Run checks

Run these commands from the repository root:

```sh
bun run lint
bun run test
```

`bun run test` starts the development server and runs the Playwright tests.
Set `PLAYWRIGHT_BASE_URL` to test an app that is already running at another
address.

To open Playwright's interactive test interface, run:

```sh
bun run test:ui
```

## Build the frontend

Run:

```sh
bun run --filter frontend build
```

The build command writes the output to `backend/app/frontend`.

## Main files

- `src/main.tsx` starts the React app.
- `src/App.tsx` contains the current app screen.
- `tests/` contains the Playwright end-to-end tests.
- `vite.config.ts` configures Vite, React, Tailwind CSS, and TanStack Router.
- `playwright.config.ts` configures the browser tests and test server.

## Current blocker

The TanStack Router plugin expects a `src/routes` directory, but that directory
does not exist. Vite startup and Playwright tests fail until the route sources
are restored or the router plugin is removed.
