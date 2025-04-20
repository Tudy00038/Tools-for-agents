<template>
  <!-- Outer column layout: chat log → sticky input area -->
  <div class="flex flex-col h-screen bg-gray-100">

    <!-- CHAT LOG (scrollable) -->
    <div class="flex-1 overflow-auto p-6 space-y-3">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="flex"
      >
        <div
          :class="[
            msg.agent === 'User'
              ? 'bg-blue-100 ml-auto'
              : 'bg-green-100 mr-auto',
            'max-w-xl p-3 rounded-lg shadow whitespace-pre-wrap'
          ]"
        >
          <strong class="block mb-1">{{ msg.agent }}:</strong>
          <div v-html="renderMarkdown(msg.result)"></div>
        </div>
      </div>
    </div>

    <!-- STICKY FOOTER -->
    <!-- STICKY FOOTER -->
<div class="sticky bottom-0 w-full bg-white border-t px-6 py-4 space-y-4">

<!-- CONDITIONAL: Model selectors shown when toggled -->
<div v-if="showModelSelectors" class="grid gap-3 md:grid-cols-2">
  <div v-for="agent in agents" :key="agent" class="flex flex-col">
    <label class="text-sm font-semibold mb-1">{{ agent }}</label>
    <select
      v-model="selectedLLMs[agent]"
      class="p-1 text-sm border rounded"
    >
      <option
        v-for="model in availableModels"
        :key="model"
        :value="model"
      >
        {{ model }}
      </option>
    </select>
  </div>
</div>

<!-- INPUT + TOGGLE BUTTON SIDE-BY-SIDE -->
<div class="flex items-center gap-2">
  <input
    v-model="prompt"
    @keyup.enter="sendPrompt"
    class="w-full p-2 text-sm border rounded shadow focus:outline-none focus:ring"
    placeholder="Type your prompt and press Enter…"
  />
  <button
    @click="showModelSelectors = !showModelSelectors"
    class="px-3 py-2 text-sm border rounded shadow bg-gray-200 hover:bg-gray-300 transition"
  >
    ⚙️ Models
  </button>
</div>
</div>

  </div>
</template>



<script setup>
import axios from 'axios';
import { marked } from 'marked';
import { ref } from 'vue';
const showModelSelectors = ref(false)

const renderMarkdown = (text) => {
  return marked(text);
};
const formatBullets = (text) => {
  return text.replace(/\*\s/g, '<br>* ');
};
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
  // 1) Push the user’s prompt as a new message (with agent: "User")
  messages.value.push({
    id: Date.now(),
    agent: "User",
    result: prompt.value // The user's typed text
  });

  // 2) Prepare payload
  const payload = {
    prompt: prompt.value,
    selected_llms: selectedLLMs.value
  };

  // Clear input
  prompt.value = "";
  showModelSelectors.value = false


  // 3) Call the backend
  try {
    const res = await axios.post('http://localhost:8000/api/query', payload);
    // 4) Now push the agent's response
    messages.value.push({
      id: Date.now() + 1,
      agent: res.data.agent,  // e.g. "Orchestrator" or "GitHub README Summarizer"
      result: res.data.result // e.g. "Delegated to ... etc"
    });
  } catch (error) {
    console.error("Error from backend:", error?.response?.data);
  }
};


</script>
<style>
/* optional: hide scrollbar on WebKit browsers for cleaner look */
.flex-1::-webkit-scrollbar {
  width: 6px;
}
.flex-1::-webkit-scrollbar-track {
  background: transparent;
}
.flex-1::-webkit-scrollbar-thumb {
  background-color: #cbd5e0; /* Tailwind gray‑400 */
  border-radius: 3px;
}
</style>

