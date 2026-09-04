import test, { expect } from "@playwright/test"
import { randomProblem } from "./utils/random"

test("Problems page is accessible and shows correct title", async ({
  page,
}) => {
  await page.goto("/problems")
  await expect(page.getByRole("heading", { name: "Problems" })).toBeVisible()
  await expect(
    page.getByText("Create and manage coding problems"),
  ).toBeVisible()
})

test("Add Problem button is visible", async ({ page }) => {
  await page.goto("/problems")
  await expect(page.getByRole("button", { name: "Add Problem" })).toBeVisible()
})

test.describe("Problems management", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/problems")
  })

  test("Add a new problem successfully", async ({ page }) => {
    const problem = randomProblem()

    await page.getByRole("button", { name: "Add Problem" }).click()
    await page.getByLabel("Title").fill(problem.title)
    await page.getByLabel("Platform").selectOption(problem.platform)
    await page.getByLabel("URL").fill(problem.url)
    await page.getByLabel("ID").fill(problem.id)
    await page.getByLabel("Difficulty").selectOption(problem.difficulty)
    await page
      .getByLabel("Norm Difficulty")
      .fill(problem.normDifficulty.toString())
    await page
      .getByLabel("Simplified Problem Statement")
      .fill(problem.simplifiedProblemStatement)
    await page.getByLabel("Notes").fill(problem.notes)
    await page.getByLabel("Solution URL").fill(problem.solutionUrl)
    await page.getByRole("button", { name: "Submit" }).click()

    await expect(page.getByText("Problem added successfully")).toBeVisible()
    await expect(page.getByText(problem.title)).toBeVisible()
  })

  test("Create problem with only required fields", async ({ page }) => {
    const problem = randomProblem()

    await page.getByRole("button", { name: "Add Problem" }).click()
    await page.getByLabel("Title").fill(problem.title)
    await page.getByLabel("Platform").selectOption(problem.platform)
    await page.getByLabel("URL").fill(problem.url)
    await page.getByLabel("ID").fill(problem.id)
    await page.getByRole("button", { name: "Submit" }).click()

    await expect(page.getByText("Problem added successfully")).toBeVisible()
    await expect(page.getByText(problem.title)).toBeVisible()
  })

  test("Cancel problem creation", async ({ page }) => {
    await page.getByRole("button", { name: "Add Problem" }).click()
    await page.getByLabel("Title").fill("Sample Problem")
    await page.getByRole("button", { name: "Cancel" }).click()

    await expect(page.getByRole("dialog")).not.toBeVisible()
  })

  test("Title is required", async ({ page }) => {
    await page.getByRole("button", { name: "Add Problem" }).click()
    await page.getByLabel("Title").fill("")
    await page.getByLabel("Title").blur()
    await page.getByRole("button", { name: "Submit" }).click()

    await expect(page.getByText("Title is required")).toBeVisible()
  })

  test.describe("Edit and Delete", () => {
    let problemTitle: string

    test.beforeEach(async ({ page }) => {
      problemTitle = randomProblem().title

      await page.getByRole("button", { name: "Add Problem" }).click()
      await page.getByLabel("Title").fill(problemTitle)
      await page.getByRole("button", { name: "Save" }).click()
      await expect(page.getByText("Problem created successfully")).toBeVisible()
      await expect(page.getByRole("dialog")).not.toBeVisible()
    })

    test("Edit a problem successfully", async ({ page }) => {
      const itemRow = page.getByRole("row").filter({ hasText: problemTitle })
      await itemRow.getByRole("button").last().click()
      await page.getByRole("menuitem", { name: "Edit Problem" }).click()

      const updatedTitle = randomProblem().title
      await page.getByLabel("Title").fill(updatedTitle)
      await page.getByRole("button", { name: "Save" }).click()

      await expect(page.getByText("Problem updated successfully")).toBeVisible()
      await expect(page.getByText(updatedTitle)).toBeVisible()
    })

    test("Delete a problem successfully", async ({ page }) => {
      const itemRow = page.getByRole("row").filter({ hasText: problemTitle })
      await itemRow.getByRole("button").last().click()
      await page.getByRole("menuitem", { name: "Delete Problem" }).click()

      await page.getByRole("button", { name: "Delete" }).click()

      await expect(
        page.getByText("The item was deleted successfully"),
      ).toBeVisible()
      await expect(page.getByText(problemTitle)).not.toBeVisible()
    })
  })
})

test.describe("Problems empty state", () => {
  test.use({ storageState: { cookies: [], origins: [] } })

  test("Shows empty state message when no problems exist", async ({ page }) => {
    await page.goto("/problems")

    await expect(
      page.getByText("You don't have any problems yet"),
    ).toBeVisible()
    await expect(
      page.getByText("Add a new problem to get started"),
    ).toBeVisible()
  })
})
