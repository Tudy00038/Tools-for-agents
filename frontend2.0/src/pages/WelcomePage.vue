<template>
    <div class="flex flex-col h-screen pb-16 md:pb-20 bg-[#f7f7f8] dark:bg-[#343541] dark:text-white">
      <!-- SCROLLABLE MAIN CONTENT -->
      <div class="flex-1 overflow-auto p-6 flex flex-col items-center text-center">
  
        <!-- TITLE -->
        <h1 class="text-3xl md:text-4xl font-bold mb-4">
          🧠 Agent Workflow Interface
        </h1>
  
        <!-- DESCRIPTION -->
        <p class="text-lg text-gray-700 dark:text-gray-300 max-w-2xl mb-8 leading-relaxed">
          This project demonstrates an AI-powered orchestration system. An orchestrator agent interprets your prompt
          and intelligently routes it to one of several specialized agents:
          <span class="font-medium">a Code Generator</span>, <span class="font-medium">a GitHub README Summarizer</span>,
          or a <span class="font-medium">Web Search Agent</span>. You can select models, interact with the agents,
          and save prompts for future use.
        </p>
  
        <!-- DIAGRAM -->
        <!-- DIAGRAM -->
<div class="w-full max-w-2xl border rounded shadow-md dark:border-gray-600 p-4 bg-white dark:bg-[#40414f]">
  <a href="/Workflow Diagram.png" target="_blank" rel="noopener noreferrer">
    <img
      src="/Workflow Diagram.png"
      alt="Agent Workflow Diagram"
      class="w-full object-contain rounded transition hover:scale-105 duration-300 cursor-pointer"
    />
  </a>
</div>
  
      </div>
    </div>
  </template>
  
  <style>
  /* Optional: match scrollbar to chat page */
  .flex-1::-webkit-scrollbar {
    width: 6px;
  }
  .flex-1::-webkit-scrollbar-track {
    background: transparent;
  }
  .flex-1::-webkit-scrollbar-thumb {
    background-color: #cbd5e0;
    border-radius: 3px;
  }
  </style>
  