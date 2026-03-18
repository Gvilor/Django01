import { createRouter, createWebHistory } from 'vue-router'
import ChannelsView from '@/views/ChannelsView.vue'
import GroupsView from '@/views/GroupsView.vue'
import ChannelTypesView from '@/views/ChannelTypesView.vue'
import DescriptionsView from '@/views/DescriptionsView.vue'
import SubscribersView from '@/views/SubscribersView.vue'
import LoginView from '@/views/LoginView.vue'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/',
    name: 'channels',
    component: ChannelsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/groups',
    name: 'groups',
    component: GroupsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/channel-types',
    name: 'channel-types',
    component: ChannelTypesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/descriptions',
    name: 'descriptions',
    component: DescriptionsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/subscribers',
    name: 'subscribers',
    component: SubscribersView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()

  if (!userStore.isAuthChecked) {
    await userStore.fetchMe()
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return '/login'
  }

  if (to.path === '/login' && userStore.isAuthenticated) {
    return '/'
  }
})

export default router