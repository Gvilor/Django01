<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const channelTypes = ref([]);
const channels = ref([]);
const selectedChannelTypeId = ref(null);
const loading = ref(false);

const channelTypesById = computed(() => {
  return _.keyBy(channelTypes.value, x => x.id)
})

const filteredChannels = computed(() => {
  if (!selectedChannelTypeId.value) {
    return channels.value;
  }

  return channels.value.filter(x => x.channel_type === selectedChannelTypeId.value);
})

async function fetchChannelTypes() {
  const r = await axios.get("/api/channel-types/");
  channelTypes.value = r.data;
}

async function fetchChannels() {
  const r = await axios.get("/api/channels/");
  channels.value = r.data;
}

onBeforeMount(async ()  => {
  loading.value = true;
  await fetchChannelTypes();
  await fetchChannels();
  loading.value = false;
})
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col">
        <div class="form-floating mb-3">
          <select class="form-select" id="channelTypeSelect" v-model="selectedChannelTypeId">
            <option :value="null">Все типы каналов</option>
            <option :value="item.id" v-for="item in channelTypes" :key="item.id">{{ item.name }}</option>
          </select>
          <label for="channelTypeSelect">Тип канала</label>
        </div>
      </div>
    </div>

    <div v-if="loading">
      Грузится...
    </div>

    <div v-for="item in filteredChannels" :key="item.id" class="channel-types-item">
      <b>{{ item.name }}</b>
      <b>{{ channelTypesById[item.channel_type]?.name || "—" }}</b>
    </div>
  </div>
</template>

<style scoped>
.channel-types-item {
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