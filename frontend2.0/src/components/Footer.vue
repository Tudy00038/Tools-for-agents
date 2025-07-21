<template>
    <footer class="w-full px-6 py-4 text-center text-sm bg-white dark:bg-[#343541] text-gray-600 dark:text-gray-400 border-t dark:border-[#2c2d30]">
      <p class="flex justify-center items-center gap-2">
        © {{ currentYear }} Iov Tudor
        <a
          href="https://www.linkedin.com/in/tudor-iov-345091226/"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-block hover:opacity-80"
        >
          <!-- LinkedIn SVG Logo -->
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor"
               class="text-blue-600 dark:text-blue-400"
               viewBox="0 0 16 16">
            <path d="M0 1.146C0 .513.324 0 .725 0h14.55c.401 
              0 .725.513.725 1.146v13.708c0 .633-.324 
              1.146-.725 1.146H.725A.723.723 0 0 
              1 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 
              0 1.358-.554 1.358-1.248-.015-.709-.52-1.247-1.341-1.247-.822 
              0-1.358.538-1.358 1.247 0 .694.52 1.248 
              1.327 1.248h.014zm4.908 8.212V9.359c0-.214.016-.428.08-.582.175-.428.574-.872 
              1.243-.872.877 0 1.228.658 1.228 1.623v3.866h2.401V9.25c0-2.22-1.183-3.252-2.762-3.252-1.274 
              0-1.845.7-2.165 1.193h.03v-1.026H6.542c.03.675 
              0 7.225 0 7.225h2.401z"/>
          </svg>
        </a>
      </p>
    </footer>
  </template>
  
  <script setup>
  const currentYear = new Date().getFullYear()
  </script>
  