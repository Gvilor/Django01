<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"

const router = useRouter()
const userStore = useUserStore()

const currentUser = computed(() => userStore.user)

onMounted(async () => {
  if (!userStore.isAuthChecked) {
    await userStore.fetchMe()
  }
})

async function onLogout() {
  try {
    await userStore.logout()
    router.push("/login")
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">TelegaChannels</router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Переключатель навигации">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto" v-if="currentUser">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Каналы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/groups">Группы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/channel-types">Типы каналов</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/descriptions">Описания</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/subscribers">Подписчики</router-link>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto" v-if="currentUser">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle d-flex align-items-center gap-2"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false">
                <span>{{ currentUser.username }}</span>
                <span class="badge text-bg-secondary">
                  {{ currentUser.is_superuser ? "admin" : "user" }}
                </span>
              </a>

              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <span class="dropdown-item-text">
                    {{ currentUser.is_superuser ? "Суперпользователь" : "Обычный пользователь" }}
                  </span>
                </li>

                <li v-if="currentUser.is_superuser">
                  <a class="dropdown-item" href="/admin/">
                    Админка
                  </a>
                </li>

                <li>
                  <button class="dropdown-item" type="button" @click="onLogout">
                    Выйти
                  </button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>

  <div class="container mt-3">
    <router-view />
  </div>
</template>

<style>
.router-link-active {
  font-weight: 600;
}
</style>