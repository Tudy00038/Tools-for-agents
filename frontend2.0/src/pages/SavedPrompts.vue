<template>
  <div class="flex flex-col h-screen pb-16 md:pb-20 bg-[#f7f7f8] dark:bg-[#343541] dark:text-white">
    <div class="flex-1 overflow-auto p-6">
      <h1 class="text-2xl font-bold mb-4 text-center">🗂 Saved Prompts</h1>

      <div class="overflow-x-auto">
        <table class="min-w-full table-auto border-collapse border border-gray-300 dark:border-gray-600">
          <thead class="bg-gray-100 dark:bg-[#3a3b43]">
            <tr>
              <th class="px-4 py-2 text-left border dark:border-gray-600">ID</th>
              <th class="px-4 py-2 text-left border dark:border-gray-600">Prompt</th>
              
              <th class="px-4 py-2 text-left border dark:border-gray-600">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in prompts"
              :key="item.id"
              class="hover:bg-gray-100 dark:hover:bg-[#444654]"
            >
              <td class="px-4 py-2 border dark:border-gray-600">{{ index + 1 }}</td>
              <td class="px-4 py-2 border dark:border-gray-600">{{ item.prompt }}</td>
              
              <td class="px-4 py-2 border dark:border-gray-600">{{ formatDate(item.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'

const prompts = ref([])

const formatDate = (datetime) => {
  return new Date(datetime).toLocaleString()
}

const fetchPrompts = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/prompts')
    prompts.value = res.data
  } catch (err) {
    console.error('Failed to fetch prompts:', err)
  }
}

onMounted(() => {
  fetchPrompts()
})
</script>

  