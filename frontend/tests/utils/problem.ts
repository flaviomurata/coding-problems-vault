import { ProblemsService } from "../../src/client"

function apiOptions() {
  const baseURL = process.env.VITE_API_URL
  if (!baseURL) {
    throw new Error(
      "Set VITE_API_URL to a dedicated test backend before running Playwright.",
    )
  }
  return { baseURL, throwOnError: true as const }
}

export async function deleteProblem(id: string) {
  await ProblemsService.deleteProblem({
    ...apiOptions(),
    path: { id },
  })
}

// This deletes all problems. Use only with a dedicated test database.
export async function deleteAllProblems() {
  const { data } = await ProblemsService.readProblems(apiOptions())
  for (const problem of data.data) {
    await deleteProblem(problem.id)
  }
}
