<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const channels = ref([]);
const groups = ref([]);
const searchText = ref("");
const loading = ref(false);

const groupsById = computed(() => {
  return _.keyBy(groups.value, x => x.id)
})

const filteredChannels = computed(() => {
  if (!searchText.value) {
    return channels.value;
  }

  return channels.value.filter(x =>
    x.description &&
    x.description.toLowerCase().includes(searchText.value.toLowerCase())
  );
})

async function fetchChannels() {
  const r = await axios.get("/api/channels/");
  channels.value = r.data;
}

async function fetchGroups() {
  const r = await axios.get("/api/groups/");
  groups.value = r.data;
}

onBeforeMount(async () => {
  loading.value = true;
  await fetchChannels();
  await fetchGroups();
  loading.value = false;
})
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col">
        <div class="form-floating mb-3">
          <input
            type="text"
            class="form-control"
            id="descriptionSearch"
            placeholder="Введите ключевое слово"
            v-model="searchText"
          >
          <label for="descriptionSearch">Поиск по описанию</label>
        </div>
      </div>
    </div>

    <div v-if="loading">
      Грузится...
    </div>

    <div v-for="item in filteredChannels" :key="item.id" class="descriptions-item">
      <div>
        <b>{{ item.name }}</b>
        <div>{{ item.description }}</div>
      </div>
      <b>{{ groupsById[item.group]?.name || "—" }}</b>
    </div>
  </div>
</template>

<style scoped>
.descriptions-item {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 16px;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
}
</style>