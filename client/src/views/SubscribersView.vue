<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const channels = ref([]);
const groups = ref([]);
const selectedFilter = ref("");
const loading = ref(false);

const groupsById = computed(() => {
  return _.keyBy(groups.value, x => x.id)
})

const filteredChannels = computed(() => {
  if (!selectedFilter.value) {
    return channels.value;
  }

  if (selectedFilter.value === "up_to_500") {
    return channels.value.filter(x => x.subscribers_count <= 500);
  }

  if (selectedFilter.value === "more_than_500") {
    return channels.value.filter(x => x.subscribers_count > 500);
  }

  if (selectedFilter.value === "more_than_1000") {
    return channels.value.filter(x => x.subscribers_count > 1000);
  }

  return channels.value;
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
          <select class="form-select" id="subscribersFilter" v-model="selectedFilter">
            <option value="">Все каналы</option>
            <option value="up_to_500">До 500 подписчиков</option>
            <option value="more_than_500">Больше 500 подписчиков</option>
            <option value="more_than_1000">Больше 1000 подписчиков</option>
          </select>
          <label for="subscribersFilter">Фильтр по подписчикам</label>
        </div>
      </div>
    </div>

    <div v-if="loading">
      Грузится...
    </div>

    <div v-for="item in filteredChannels" :key="item.id" class="subscribers-item">
      <div>
        <b>{{ item.name }}</b>
        <div>{{ item.description }}</div>
      </div>

      <div class="subscribers-meta">
        <b>{{ groupsById[item.group]?.name || "—" }}</b>
        <b>{{ item.subscribers_count }}</b>
      </div>
    </div>
  </div>
</template>

<style scoped>
.subscribers-item {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 16px;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
}

.subscribers-meta {
  display: grid;
  gap: 4px;
  text-align: right;
}
</style>