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

 
  <div v-for="msg in messages" :key="msg.id" class="bg-white rounded shadow p-3">
    <strong>{{ msg.agent }}:</strong>
    <div v-html="renderMarkdown(msg.result)"></div>
  </div>
  <div v-for="msg in messages" :key="msg.id" class="my-2 flex">
  <!-- If agent is "User", put it on the right. If agent is not "User", put it on the left. -->
  <div 
    :class="[
      msg.agent === 'User' ? 'bg-blue-100 ml-auto' : 'bg-green-100 mr-auto',
      'max-w-lg','p-3','rounded','shadow'
    ]"
  >
    <strong>{{ msg.agent }}</strong>
    <div v-html="renderMarkdown(msg.result)"></div>
  </div>
</div>
</template>

<script setup>
import axios from 'axios';
import { marked } from 'marked';
import { ref } from 'vue';
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
