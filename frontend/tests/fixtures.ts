import { test as base, expect } from "@playwright/test"
import { deleteAllProblems } from "./utils/problem"

export const test = base.extend<{ problemIsolation: undefined }>({
  problemIsolation: [
    // biome-ignore lint/correctness/noEmptyPattern: Playwright requires destructuring to identify fixture dependencies.
    async ({}, use) => {
      await deleteAllProblems()
      try {
        await use(undefined)
      } finally {
        await deleteAllProblems()
      }
    },
    { auto: true },
  ],
})

export { expect }
