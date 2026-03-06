<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const channels = ref([]);
const groups = ref([]);
const channelTypes = ref([]);
const channelsToAdd = ref({});
const channelsToEdit = ref({});
const loading = ref(false);

const groupsById = computed(() => {
  return _.keyBy(groups.value, x => x.id)
})

const channelTypesById = computed(() => {
  return _.keyBy(channelTypes.value, x => x.id)
})

async function fetchGroups() {
  const r = await axios.get("/api/groups/")
  groups.value = r.data;
}

async function fetchChannelTypes() {
  const r = await axios.get("/api/channel-types/")
  channelTypes.value = r.data;
}

async function fetchChannels() {
  const r = await axios.get("/api/channels/")
  channels.value = r.data;
}

async function onChannelsAdd() {
  await axios.post("/api/channels/", {
    ...channelsToAdd.value,
  });
  channelsToAdd.value = {};
  await fetchChannels();
}

async function onRemoveClick(channel) {
  await axios.delete(`/api/channels/${channel.id}/`)
  await fetchChannels();
}

async function onChannelEditClick(channel) {
  channelsToEdit.value = { ...channel };
}

async function onUpdateChannel() {
  await axios.put(`/api/channels/${channelsToEdit.value.id}/`, {
    ...channelsToEdit.value
  })
  await fetchChannels();
}

onBeforeMount(async ()  => {
  loading.value = true;
  await fetchChannels();
  await fetchGroups();
  await fetchChannelTypes();
  loading.value = false;
})
</script>

<template>
  <div class="modal fade" id="editChannelModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">Редактирование канала</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>

        <div class="modal-body">
          <div class="row">
            <div class="col-12 col-md-6">
              <div class="form-floating mb-3">
                <input type="text" class="form-control" v-model="channelsToEdit.name" id="editChannelName" placeholder="Название канала">
                <label for="editChannelName">Название канала</label>
              </div>
            </div>

            <div class="col-12 col-md-6">
              <div class="form-floating mb-3">
                <select class="form-select" id="editGroupSelect" v-model="channelsToEdit.group">
                  <option :value="g.id" v-for="g in groups" :key="g.id">{{ g.name }}</option>
                </select>
                <label for="editGroupSelect">Группа</label>
              </div>
            </div>

            <div class="col-12 col-md-6">
              <div class="form-floating mb-3">
                <select class="form-select" id="editChannelTypeSelect" v-model="channelsToEdit.channel_type">
                  <option :value="item.id" v-for="item in channelTypes" :key="item.id">{{ item.name }}</option>
                </select>
                <label for="editChannelTypeSelect">Тип канала</label>
              </div>
            </div>

            <div class="col-12 col-md-6">
              <div class="form-floating mb-3">
                <input
                  type="number"
                  class="form-control"
                  v-model="channelsToEdit.subscribers_count"
                  id="editSubscribersCount"
                  placeholder="Количество подписчиков"
                >
                <label for="editSubscribersCount">Количество подписчиков</label>
              </div>
            </div>

            <div class="col-12">
              <div class="form-floating mb-3">
                <textarea
                  class="form-control"
                  v-model="channelsToEdit.description"
                  id="editDescription"
                  placeholder="Описание канала"
                  style="height: 120px"
                ></textarea>
                <label for="editDescription">Описание канала</label>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateChannel">Сохранить изменения</button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent="onChannelsAdd">
      <div class="row">
        <div class="col-12 col-md-4">
          <div class="form-floating mb-3">
            <input
              type="text"
              class="form-control"
              v-model="channelsToAdd.name"
              id="channelName"
              placeholder="Название канала"
              required
            >
            <label for="channelName">Название канала</label>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="form-floating mb-3">
            <select class="form-select" id="groupSelect" v-model="channelsToAdd.group" required>
              <option :value="g.id" v-for="g in groups" :key="g.id">{{ g.name }}</option>
            </select>
            <label for="groupSelect">Группа</label>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="form-floating mb-3">
            <select class="form-select" id="channelTypeSelect" v-model="channelsToAdd.channel_type" required>
              <option :value="item.id" v-for="item in channelTypes" :key="item.id">{{ item.name }}</option>
            </select>
            <label for="channelTypeSelect">Тип канала</label>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="form-floating mb-3">
            <input
              type="number"
              class="form-control"
              v-model="channelsToAdd.subscribers_count"
              id="subscribersCount"
              placeholder="Количество подписчиков"
              required
            >
            <label for="subscribersCount">Количество подписчиков</label>
          </div>
        </div>

        <div class="col-12 col-md-8">
          <div class="form-floating mb-3">
            <textarea
              class="form-control"
              v-model="channelsToAdd.description"
              id="channelDescription"
              placeholder="Описание канала"
              style="height: 120px"
              required
            ></textarea>
            <label for="channelDescription">Описание канала</label>
          </div>
        </div>

        <div class="col-12">
          <button type="submit" class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-if="loading">
      Грузится...
    </div>

    <div v-for="item in channels" :key="item.id" class="channels-item">
      <div class="channel-main">
        <b>{{ item.name }}</b>
        <div>{{ item.description }}</div>
      </div>

      <div class="channel-meta">
        <span>{{ groupsById[item.group]?.name || "—" }}</span>
        <span>{{ channelTypesById[item.channel_type]?.name || "—" }}</span>
        <span>{{ item.subscribers_count }}</span>
      </div>

      <button
        type="button"
        class="btn btn-success"
        @click="onChannelEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editChannelModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>

      <button type="button" class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-trash-fill"></i>
      </button>
    </div>
  </div>
</template>

<style lang="css" scoped>
.channels-item {
  display: grid;
  grid-template-columns: 2fr 1.5fr auto auto;
  align-items: center;
  gap: 16px;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
}

.channel-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.channel-meta {
  display: grid;
  gap: 4px;
}
</style>