<template>
  <div class="flex flex-col h-screen bg-gray-100 p-6">
    <div class="overflow-auto flex-1 space-y-2">
      <div v-for="msg in messages" :key="msg.id" class="bg-white rounded shadow p-3">
        <strong>{{ msg.agent }}:</strong> {{ msg.result }}
      </div>
    </div>

    <div class="mt-4">
      <div v-for="agent in agents" :key="agent" class="mb-2">
        <label>{{ agent }}</label>
        <select v-model="selectedLLMs[agent]" class="p-2 border rounded w-full">
          <option v-for="model in availableModels" :key="model" :value="model">{{ model }}</option>
        </select>
      </div>

      <input v-model="prompt" @keyup.enter="sendPrompt" class="w-full p-3 rounded border shadow" placeholder="Type your prompt..." />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const prompt = ref('')
const messages = ref([])

const agents = ["GitHub README Summarizer", "Search Web Agent", "Code Generator Agent"]
const availableModels = ["gemma3:latest", "qwen2.5-coder:3b"]

const selectedLLMs = ref({
  "orchestrator": "gemma3:latest",
    "code_generator": "qwen2.5-coder:3b",  
    "search_web": "gemma3:latest",
    "github_readme": "gemma3:latest",
})

const sendPrompt = async () => {
  const payload = {
    prompt: prompt.value,
    selected_llms: selectedLLMs.value
  };

  console.log("Payload sent:", payload); // Debug payload

  try {
    const res = await axios.post('http://localhost:8000/api/query', payload);
    messages.value.push({
      id: Date.now(),
      agent: res.data.agent,
      result: res.data.result
    });
  } catch (error) {
    console.error("Error from backend:", error.response.data);
  }

  prompt.value = '';
}

</script>
