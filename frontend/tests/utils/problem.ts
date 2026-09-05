import { ProblemsService } from "@/client"

export async function deleteProblem(id: string) {
  await ProblemsService.deleteProblem({
    path: { id },
  })
}
