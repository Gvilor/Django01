<script setup>
import {computed, ref, onBeforeMount} from 'vue'; 
import axios from 'axios';
import _, { startCase } from 'lodash';

const channels = ref([]);
const groups = ref([]);
const channelsToAdd = ref({});
const channelsToEdit = ref({});



const loading = ref(false);

const groupsById = computed(() => {
  return _.keyBy(groups.value, x => x.id)
})



async function fetchGroups() {
  const r = await axios.get("/api/groups/")
  groups.value = r.data;
}

async function fetchChannels() {
  const r = await axios.get("/api/channels/")
  channels.value = r.data;
}

async function onChannelsAdd() {
  await axios.post("/api/channels/", {
    ...channelsToAdd.value,
  });
  await fetchChannels();
}

async function onRemoveClick(channels) {
  await axios.delete(`/api/channels/${channels.id}/`) 
  await fetchChannels();

}

async function onChannelEditClick(channels) {
  channelsToEdit.value = {...channels};
}

async function onUpdateChannel() {
  await axios.put(`/api/channels/${channelsToEdit.value.id}/`, {
    ...channelsToEdit.value
  }) 
  await fetchChannels();
}

onBeforeMount(async ()  => {
  await fetchChannels();
  await fetchGroups();

})

</script>

<template>

  
  <!-- Модальное окно -->
<div class="modal fade" id="editChannelModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Заголовок модального окна</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
      </div>
      <div class="modal-body">
        <div class="row">
    <div class="col">
        <div class="form-floating mb-3">
          <input type="text" class="form-control" v-model="channelsToEdit.name" id="channelName" placeholder="Название канала">
          <label for="channelName">Название канала</label>
        </div>
    </div>
    <div class="col-auto">
      <div class="form-floating mb-3">
        <select class="form-select" id="groupSelect" v-model="channelsToEdit.group">
            <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
        </select>
        <label for="groupSelect">Группа</label>
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
    <div class="col">
        <div class="form-floating mb-3">
          <input type="text" class="form-control" v-model="channelsToAdd.name" id="channelName" placeholder="Название канала" required>
          <label for="channelName">Название канала</label>
        </div>
    </div>
    <div class="col-auto">
      <div class="form-floating mb-3">
        <select class="form-select" id="groupSelect" v-model="channelsToAdd.group" required>
            <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
        </select>
        <label for="groupSelect">Группа</label>
      </div>
    </div>
    <div class="col-auto">
      <button type="submit" class="btn btn-primary">Добавить</button>
    </div>
  </div>
  </form>





  <div v-if="loading"> 
    Грузится...
  </div>

  <div v-for="item in channels" class ="channels-item">
    <b> {{item.name }}</b> <b>{{ groupsById[item.group]?.name}}</b> 
    <button type="button" class="btn btn-success" @click="onChannelEditClick(item)" data-bs-toggle="modal" data-bs-target="#editChannelModal"><i class="bi bi-pen-fill"></i></button>
    <button type="button" class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-trash-fill"></i></button>
  </div>
</div>

</template>

<style lang="css" scoped>
  .channels-item {
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    align-items: center;
    gap: 16px;
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;

  }
</style>
 