export const randomProblem = () => {
  const title = `Sample Problem ${Math.random().toString(36).substring(7)}`
  const platform = ["Codeforces", "LeetCode", "HackerRank"][
    Math.floor(Math.random() * 3)
  ]
  const url = `https://${platform}.com/problem/${Math.floor(Math.random() * 1000)}/A`
  const id = `${Math.floor(Math.random() * 1000)}`
  const difficulty = ["easy", "medium", "hard"][Math.floor(Math.random() * 3)]
  const normDifficulty = Math.floor(Math.random() * 10) + 1 // Random difficulty between 1 and 5
  const simplifiedProblemStatement = Math.random().toString(36).substring(7)
  const notes = Math.random().toString(36).substring(7)
  const solutionUrl = `https://github.com/solution/${Math.floor(Math.random() * 1000)}`

  return {
    title,
    platform,
    url,
    id,
    difficulty,
    normDifficulty,
    simplifiedProblemStatement,
    notes,
    solutionUrl,
  }
}
