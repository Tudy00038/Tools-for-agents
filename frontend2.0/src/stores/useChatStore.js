import { ref } from 'vue'

const messages = ref([])
const prompt = ref('')
const selectedLLMs = ref({
  orchestrator: 'gemma3:latest',
  code_generator: 'qwen2.5-coder:3b',
  search_web: 'gemma3:latest',
  github_readme: 'gemma3:latest',
})

const showModelSelectors = ref(false)
const currentAgent = ref('')

export function useChatStore() {
  return {
    messages,
    prompt,
    selectedLLMs,
    showModelSelectors,
    currentAgent
  }
}
