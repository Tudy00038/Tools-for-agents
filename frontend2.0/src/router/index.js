import { createRouter, createWebHistory } from 'vue-router'

// Page components (we’ll create them next)
import ChatInterface from '../pages/ChatInterface.vue'
import SavedPrompts from '../pages/SavedPrompts.vue'
import WelcomePage from '../pages/WelcomePage.vue'

const routes = [
  { path: '/', name: 'Welcome', component: WelcomePage },
  { path: '/chat', name: 'Chat', component: ChatInterface },
  { path: '/prompts', name: 'SavedPrompts', component: SavedPrompts },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
