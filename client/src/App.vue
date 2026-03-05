<script setup> 


</script>

<template>

  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">TelegaChannels</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Переключатель навигации">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/"> Каналы </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/groups"> Группы </router-link>
        </li>
      </ul>
      </div>
    </div>
  </nav>
</div>
<div class="container">
  <router-view/>
</div>
</template>

<style>



</style>