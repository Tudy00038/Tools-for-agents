<template>
    <nav class="bg-white dark:bg-[#343541] border-b dark:border-[#2c2d30] shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
         <!-- Replace title with logo -->
      <router-link to="/" class="flex items-center gap-2">
        <img
          src="/Logo_Licenta2-removebg-preview.png"
          alt="App Logo"
          class="w-12 max-h-10 object-contain scale-110"
          style="margin-top: -2px;"
        />
        <span class="sr-only">Agent App</span> <!-- for screen readers -->
      </router-link>
        <div class="flex gap-4">
          <router-link
            to="/"
            class="text-gray-700 dark:text-gray-200 hover:underline"
            :class="{ 'font-bold underline': route.path === '/' }"
          >
            Welcome
          </router-link>
          <router-link
            to="/chat"
            class="text-gray-700 dark:text-gray-200 hover:underline"
            :class="{ 'font-bold underline': route.path === '/chat' }"
          >
            Chat
          </router-link>
          <router-link
            to="/prompts"
            class="text-gray-700 dark:text-gray-200 hover:underline"
            :class="{ 'font-bold underline': route.path === '/prompts' }"
          >
            Saved Prompts
          </router-link>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { useRoute } from 'vue-router';
  const route = useRoute()
  </script>
  