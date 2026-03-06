<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

const groups = ref([]);
const channels = ref([]);
const selectedGroupId = ref(null);
const groupToAdd = ref({});
const groupToEdit = ref({});
const loading = ref(false);

const filteredChannels = computed(() => {
  if (!selectedGroupId.value) {
    return channels.value;
  }

  return channels.value.filter(x => x.group === selectedGroupId.value);
});

async function fetchGroups() {
  const r = await axios.get("/api/groups/");
  groups.value = r.data;
}

async function fetchChannels() {
  const r = await axios.get("/api/channels/");
  channels.value = r.data;
}

async function onGroupAdd() {
  await axios.post("/api/groups/", {
    ...groupToAdd.value,
  });
  groupToAdd.value = {};
  await fetchGroups();
}

async function onGroupEditClick(group) {
  groupToEdit.value = { ...group };
}

async function onUpdateGroup() {
  await axios.put(`/api/groups/${groupToEdit.value.id}/`, {
    ...groupToEdit.value,
  });
  await fetchGroups();
}

async function onRemoveClick(group) {
  await axios.delete(`/api/groups/${group.id}/`);
  await fetchGroups();

  if (selectedGroupId.value === group.id) {
    selectedGroupId.value = null;
  }
}

onBeforeMount(async () => {
  loading.value = true;
  await fetchGroups();
  await fetchChannels();
  loading.value = false;
});
</script>

<template>
  <div class="modal fade" id="addGroupModal" tabindex="-1" aria-labelledby="addGroupModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="addGroupModalLabel">Добавление группы</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="onGroupAdd">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                id="groupName"
                placeholder="Название группы"
                v-model="groupToAdd.name"
                required
              >
              <label for="groupName">Название группы</label>
            </div>

            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">
              Добавить
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="editGroupModal" tabindex="-1" aria-labelledby="editGroupModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="editGroupModalLabel">Редактирование группы</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="onUpdateGroup">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                id="editGroupName"
                placeholder="Название группы"
                v-model="groupToEdit.name"
                required
              >
              <label for="editGroupName">Название группы</label>
            </div>

            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">
              Сохранить изменения
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid">
    <div class="row mb-3">
      <div class="col">
        <div class="form-floating">
          <select class="form-select" id="groupSelect" v-model="selectedGroupId">
            <option :value="null">Все группы</option>
            <option :value="g.id" v-for="g in groups" :key="g.id">
              {{ g.name }}
            </option>
          </select>
          <label for="groupSelect">Выберите группу</label>
        </div>
      </div>

      <div class="col-auto">
        <button
          type="button"
          class="btn btn-primary h-100"
          data-bs-toggle="modal"
          data-bs-target="#addGroupModal"
        >
          Добавить
        </button>
      </div>
    </div>

    <div v-if="loading">
      Грузится...
    </div>

    <div v-for="item in groups" :key="item.id" class="groups-item">
      <b>{{ item.name }}</b>

      <button
        type="button"
        class="btn btn-success"
        @click="onGroupEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editGroupModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>

      <button type="button" class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-trash-fill"></i>
      </button>
    </div>

    <hr class="my-4" />

    <div v-for="item in filteredChannels" :key="item.id" class="channels-item">
      <b>{{ item.name }}</b>
    </div>
  </div>
</template>

<style scoped>
.groups-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 16px;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
}

.channels-item {
  display: grid;
  grid-template-columns: 1fr;
  align-items: center;
  gap: 16px;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
}
</style>