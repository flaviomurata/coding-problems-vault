import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import "./index.css"
import {
  MutationCache,
  QueryCache,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query"
import { AxiosError } from "axios"
import App from "./App.tsx"
import { client } from "./client/client.gen"

client.setConfig({
  baseURL: import.meta.env.VITE_API_URL ?? "",
})

const handleApiError = (error: Error) => {
  if (
    error instanceof AxiosError &&
    [401, 403].includes(error.response?.status ?? 0)
  ) {
    localStorage.removeItem("access_token")
    window.location.href = "/login"
  }
}
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: handleApiError,
  }),
  mutationCache: new MutationCache({
    onError: handleApiError,
  }),
})

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
