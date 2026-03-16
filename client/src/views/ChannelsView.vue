<script setup>
import { computed, ref, onBeforeMount } from 'vue'
import axios from 'axios'
import _ from 'lodash'

const channels = ref([])
const groups = ref([])
const channelTypes = ref([])
const channelsToAdd = ref({})
const channelsToEdit = ref({})
const loading = ref(false)
const errorMessage = ref('')
const stats = ref(null)

const channelsPictureRef = ref()
const channelAddImageUrl = ref(null)

const channelEditPictureRef = ref()
const channelEditImageUrl = ref(null)

const selectedImage = ref(null)

const groupsById = computed(() => {
  return _.keyBy(groups.value, x => x.id)
})

const channelTypesById = computed(() => {
  return _.keyBy(channelTypes.value, x => x.id)
})

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop().split(';').shift()
  }
  return null
}

function openImage(url) {
  selectedImage.value = url
}

function closeImage() {
  selectedImage.value = null
}

async function fetchGroups() {
  const r = await axios.get('/api/groups/')
  groups.value = r.data
}

async function fetchChannelTypes() {
  const r = await axios.get('/api/channel-types/')
  channelTypes.value = r.data
}

async function fetchChannels() {
  try {
    const r = await axios.get('/api/channels/', {
      withCredentials: true
    })
    channels.value = r.data
    errorMessage.value = ''
  } catch (error) {
    channels.value = []
    errorMessage.value = 'Чтобы просматривать каналы, нужно войти в систему.'
  }
}

async function fetchStats() {
  try {
    const r = await axios.get('/api/channels/stats/', {
      withCredentials: true
    })
    stats.value = r.data
  } catch (error) {
    stats.value = null
  }
}

async function onChannelsAdd() {
  try {
    const formData = new FormData()

    if (channelsPictureRef.value?.files?.[0]) {
      formData.append('picture', channelsPictureRef.value.files[0])
    }

    formData.set('name', channelsToAdd.value.name || '')
    formData.set('description', channelsToAdd.value.description || '')
    formData.set('group', channelsToAdd.value.group || '')
    formData.set('channel_type', channelsToAdd.value.channel_type || '')
    formData.set('subscribers_count', channelsToAdd.value.subscribers_count || 0)

    await axios.post('/api/channels/', formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': getCookie('csrftoken'),
      }
    })

    channelsToAdd.value = {}
    channelAddImageUrl.value = null

    if (channelsPictureRef.value) {
      channelsPictureRef.value.value = null
    }

    await fetchChannels()
    await fetchStats()
  } catch (error) {
    errorMessage.value = 'Не удалось добавить канал.'
  }
}

async function onRemoveClick(channel) {
  try {
    await axios.delete(`/api/channels/${channel.id}/`, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
})
    await fetchChannels()
    await fetchStats()
  } catch (error) {
    errorMessage.value = 'Не удалось удалить канал.'
  }
}

async function onChannelEditClick(channel) {
  channelsToEdit.value = { ...channel }
  channelEditImageUrl.value = channel.picture || null

  if (channelEditPictureRef.value) {
    channelEditPictureRef.value.value = null
  }
}

async function onUpdateChannel() {
  try {
    const formData = new FormData()

    if (channelEditPictureRef.value?.files?.[0]) {
      formData.append('picture', channelEditPictureRef.value.files[0])
    }

    formData.set('name', channelsToEdit.value.name || '')
    formData.set('description', channelsToEdit.value.description || '')
    formData.set('group', channelsToEdit.value.group || '')
    formData.set('channel_type', channelsToEdit.value.channel_type || '')
    formData.set('subscribers_count', channelsToEdit.value.subscribers_count || 0)

    await axios.patch(`/api/channels/${channelsToEdit.value.id}/`, formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': getCookie('csrftoken'),
      }
})

    channelsToEdit.value = {}
    channelEditImageUrl.value = null

    if (channelEditPictureRef.value) {
      channelEditPictureRef.value.value = null
    }

    await fetchChannels()
    await fetchStats()
  } catch (error) {
    console.log('Ошибка обновления:', error)
    console.log('Ответ сервера:', error.response?.data)
    errorMessage.value = JSON.stringify(error.response?.data || 'Не удалось обновить канал.')
}
}

function channelsAddPictureChange() {
  if (channelsPictureRef.value?.files?.[0]) {
    channelAddImageUrl.value = URL.createObjectURL(channelsPictureRef.value.files[0])
  }
}

function channelsEditPictureChange() {
  if (channelEditPictureRef.value?.files?.[0]) {
    channelEditImageUrl.value = URL.createObjectURL(channelEditPictureRef.value.files[0])
  }
}

onBeforeMount(async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    await fetchGroups()
    await fetchChannelTypes()
    await fetchChannels()
    await fetchStats()
  } finally {
    loading.value = false
  }
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
                <input
                  type="text"
                  class="form-control"
                  v-model="channelsToEdit.name"
                  id="editChannelName"
                  placeholder="Название канала">
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
                  placeholder="Количество подписчиков">
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
                  style="height: 120px"></textarea>
                <label for="editDescription">Описание канала</label>
              </div>
            </div>

            <div class="col-12 col-md-6">
              <input
                class="form-control mb-3"
                type="file"
                ref="channelEditPictureRef"
                @change="channelsEditPictureChange">
            </div>

            <div class="col-12 col-md-6" v-if="channelEditImageUrl">
              <img
                :src="channelEditImageUrl"
                style="max-height: 60px; cursor: pointer;"
                @click="openImage(channelEditImageUrl)">
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateChannel">
            Сохранить изменения
          </button>
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
              required>
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
              required>
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
              required>
            </textarea>
            <label for="channelDescription">Описание канала</label>
          </div>
        </div>

        <div class="col-auto">
          <input
            class="form-control mb-3"
            type="file"
            ref="channelsPictureRef"
            @change="channelsAddPictureChange">
        </div>

        <div class="col-auto" v-if="channelAddImageUrl">
          <img
            :src="channelAddImageUrl"
            style="max-height: 60px; cursor: pointer;"
            @click="openImage(channelAddImageUrl)">
        </div>

        <div class="col-12 mb-3">
          <button type="submit" class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-if="loading">
      Грузится...
    </div>

    <div v-if="errorMessage" class="alert alert-warning">
      {{ errorMessage }}
    </div>

    <div v-if="stats" class="alert alert-info">
      <div><b>Статистика по каналам</b></div>
      <div>Количество каналов: {{ stats.count }}</div>
      <div>Среднее число подписчиков: {{ stats.avg ? Number(stats.avg).toFixed(2) : '—' }}</div>
      <div>Максимум подписчиков: {{ stats.max ?? '—' }}</div>
      <div>Минимум подписчиков: {{ stats.min ?? '—' }}</div>
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

      <div v-show="item.picture">
        <img
          :src="item.picture"
          style="max-height: 60px; cursor: pointer;"
          @click="openImage(item.picture)"
        >
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

  <div v-if="selectedImage" class="image-modal" @click="closeImage">
    <img :src="selectedImage" class="image-modal-content">
  </div>
</template>

<style lang="css" scoped>
.channels-item {
  display: grid;
  grid-template-columns: 2fr 1.5fr auto auto auto;
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

.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-modal-content {
  max-height: 90%;
  max-width: 90%;
}
</style>