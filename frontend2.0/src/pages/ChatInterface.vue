<template>
    <!-- Outer column layout: chat log → sticky input area -->
    <div class="flex flex-col  pb-16 md:pb-20 bg-[#f7f7f8] dark:bg-[#343541] dark:text-gray-100">
  
      <!-- CHAT LOG -->
  <div class="flex-1 overflow-auto p-6 space-y-3">
    <div v-if="messages.length === 0" class="text-center text-gray-400 mt-12">
      👋 Hi there!  Selecting the models you want to use and ask the agent something.
    </div>
  
    <div
      v-for="msg in messages"
      :key="msg.id"
      class="flex"
    >
      <div
      :class="[
    msg.agent === 'User'
      ? 'bg-blue-100 text-blue-800 dark:bg-[#3e3f4b] dark:text-[#f7f7f8] ml-auto'
      : 'bg-green-100 text-green-800 dark:bg-[#444654] dark:text-[#ececf1] mr-auto',
    'max-w-xl p-3 rounded-lg shadow-sm whitespace-pre-wrap'
  ]"
      >
        <strong class="block mb-1">{{ msg.agent }}:</strong>
        <div v-html="renderMarkdown(msg.result)"></div>
      </div>
    </div>
  </div>
  
      <!-- STICKY FOOTER -->
  <div class="sticky bottom-0 w-full bg-[#f7f7f8] dark:bg-[#343541] dark:text-gray-100 border-t px-6 py-4 space-y-4">
  
  <!-- CONDITIONAL: Model selectors shown when toggled -->
  <div v-if="showModelSelectors" class="grid gap-3 md:grid-cols-2">
    <div v-for="agent in agents" :key="agent" class="flex flex-col">
      <label class="text-sm font-semibold mb-1">{{ agent }}</label>
      <select
    v-model="selectedLLMs[agent]"
    class="p-2 text-sm border rounded
           bg-white text-black border-gray-300
           dark:bg-[#40414f] dark:text-[#f7f7f8] dark:border-[#565869]"
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
  <!-- INPUT + BUTTONS -->
<div class="flex items-center gap-2">
  <input
    v-model="prompt"
    @keyup.enter="sendPrompt"
    class="w-full p-2 text-sm border rounded shadow-sm focus:outline-none focus:ring
           bg-white text-black border-gray-300
           dark:bg-[#40414f] dark:border-[#565869] dark:text-[#f7f7f8] dark:placeholder-gray-400"
    placeholder="Type your prompt and press Enter…"
  />
  
  <!-- ⚙️ Models -->
  <button
    @click="showModelSelectors = !showModelSelectors"
    class="px-4 py-2 text-sm rounded-md shadow-sm transition font-medium
           bg-gray-200 text-gray-800 hover:bg-gray-300
           dark:bg-[#444654] dark:text-[#f7f7f8] dark:hover:bg-[#565869]"
  >
    ⚙️ Models
  </button>

  <!-- 💾 Save -->
  <button
    @click="savePromptToDB"
    class="px-4 py-2 text-sm rounded-md shadow-sm transition font-medium
           bg-green-200 text-green-900 hover:bg-green-300
           dark:bg-green-800 dark:text-white dark:hover:bg-green-700"
  >
    💾 Save
  </button>
</div>

  </div>
  
    </div>
  </template>
  
  
  
  <script setup>
  import axios from 'axios';
import { marked } from 'marked';
import { ref } from 'vue';
import { useChatStore } from '../stores/useChatStore';
  //const showModelSelectors = ref(false)
  //const currentAgent = ref("")
import { useToast } from 'vue-toastification';
const toast = useToast()
  
  const renderMarkdown = (text) => {
    return marked(text);
  };
  const formatBullets = (text) => {
    return text.replace(/\*\s/g, '<br>* ');
  };
  const{
    messages,
    prompt,
    selectedLLMs,
    showModelSelectors,
    currentAgent
  } = useChatStore()
  //const prompt = ref('')
  //const messages = ref([])
  
  const agents = ["GitHub README Summarizer", "Search Web Agent", "Code Generator Agent"]
  const availableModels = ["gemma3:latest", "qwen2.5-coder:3b","llama3.2:latest","mistral:latest"]
  
  // const selectedLLMs = ref({
  //   "orchestrator": "gemma3:latest",
  //     "code_generator": "qwen2.5-coder:3b",  
  //     "search_web": "gemma3:latest",
  //     "github_readme": "gemma3:latest",
  // })
  
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
      currentAgent.value = res.data.agent
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
  const savePromptToDB = async () => {
  if (!prompt.value.trim()) {
    toast.warning("⚠️ Please type a prompt first.")
    return
  }

  try {
    await axios.post('http://localhost:8000/api/save_prompt', {
      prompt: prompt.value
    })
    toast.success("✅ Prompt saved!")
  } catch (err) {
    if (err.response?.status === 409) {
      toast.warning("⚠️ Prompt already exists.")
    } else {
      console.error("Save failed:", err)
      toast.error("❌ Failed to save prompt.")
    }
  }
}



  
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
  
  