<script setup>
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
          aria-label="Переключатель навигации"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
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
        </div>

        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Пользователь
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
            </ul>
          </li>
        </ul>
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