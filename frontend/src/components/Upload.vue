<script setup>

import { ref, onMounted } from 'vue';
import moment from 'moment';

const fileTypes =  [
  {'value': 'unknown', 'text': 'Ukendt'},
  {'value': 'tablets_knox', 'text': 'Samsung Knox'},
  {'value': 'video_calls', 'text': 'Vitacomm'},
  {'value': 'citizens', 'text': 'Borgere'},
  {'value': 'tablets_nexus', 'text': 'Skærme'}
];

const selectedFileType = ref({'value': 'unknown', 'text': 'Ukendt'});
const knownFileType = ref(false);
const fileSelected = ref(false);
const file = ref(null);
const msg = ref(null)

let now = new Date();
let time_offset = now.getMinutes() - now.getTimezoneOffset();
now.setMinutes(time_offset);
const dateTime = ref(now.toISOString().slice(0, 16));

let lastWeek = new Date();
lastWeek.setDate(lastWeek.getDate() - 7);
const yearWeek = ref(now.getFullYear() + "-W" + (moment(lastWeek).isoWeek()));

function onFileChanged($event) {
  fileSelected.value = $event.target.files.length < 1 ? false : true;
  
  if ($event.target.files.length > 0){
    let temp_fn = $event.target.files[0].name.split('.');
    temp_fn.pop();
    const file_name = temp_fn.join('.')
    if (file_name.includes('video')) {
        selectedFileType.value = fileTypes[2];
    } else if (file_name.includes('Device_List')) {
        // get time from default Knox file name
        let time_str = file_name.split("_").slice(-1)[0];
        let time_of_creation = moment(time_str, 'YYYY-MM-DD HH.mm.ss').format("YYYY-MM-DDTkk:mm").toString();
        dateTime.value = time_of_creation
        selectedFileType.value = fileTypes[1];
    } else if (file_name.includes('borger')) {
        selectedFileType.value = fileTypes[3];
    } else if (file_name.includes('skærm')) {
        selectedFileType.value = fileTypes[4];
    }else {
        selectedFileType.value === fileTypes[0];
    }
  }

  file.value = $event.target.files[0]

  checkFileType();
}

function checkFileType() {
  knownFileType.value = selectedFileType.value.value === 'unknown' ? false : true;
}

function submitDisabled() {
  return !(knownFileType.value && fileSelected.value);
}

async function submitFile() {
  msg.value = '';
  let formData = new FormData()
  formData.append('file', file.value);
  formData.append('filetype', selectedFileType.value.value);
  formData.append('datetime', dateTime.value);
  formData.append('week', yearWeek.value);

  const response = await fetch("/file-upload", { method: "POST", body: formData });
  const res = await response.json();

  msg.value = res.message;
}

function chooseFiles() {
  document.getElementById("fileUpload").click()
}

</script>

<template>
<div class="upload">
  <h1>Upload fil</h1>
  <h2>{{msg}}</h2>
    <form v-on:submit.prevent="submitFile">
      <input id="fileUpload" @change="onFileChanged($event)" ref="fileInput" type="file" accept=".csv" class="file-input">
      <div class="form-group">
        <label for="filetype">Filtype</label>
        <select @change="checkFileType()" v-model="selectedFileType.value" class="file-type-select">
          <option v-for="type in fileTypes" :key="type.value" :value="type.value" class="file-type-select">{{type.text}}</option>
        </select>
      </div>
      <input v-show="selectedFileType.value === 'tablets_knox'" v-model="dateTime" type="datetime-local" class="time-input">
      <input v-show="selectedFileType.value === 'citizens' || selectedFileType.value === 'tablets_nexus'" v-model="yearWeek" type="week" class="time-input">
      <input :disabled="submitDisabled()" type="submit" value="Upload" class="submit-button">
  </form>
</div>

</template>

<style scoped>
@media (min-width: 512px) {
  .upload {
    display: flex;
    align-items: center;
    flex-direction: column;
  }
}

form {
  min-width: 400px;
}

.form-group {
  display: flex;
  flex-direction: row;
  margin-top: 10px;
}

label {
  color: var(--vt-c-blue);
  padding: 10px;
  font-size: 14px;
  font-weight: bold;
}

h3 {
  color: var(--vt-c-blue);
  padding: 10px;
  font-size: 14px;
  font-weight: bold;
}

.file-type-select {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--vt-c-grey);
  border-radius: 5px;
}

.time-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--vt-c-grey);
  border-radius: 5px;
  margin-top: 10px;
}

.file-input {
  width: 100%;
}

input[type="file"]::file-selector-button {
  border-radius: 4px;
  padding: 0 16px;
  height: 35px;
  cursor: pointer;
  background-color:var(--vt-c-blue);
  color: var(--vt-c-white);
  border: 1px solid rgba(0, 0, 0, 0.16);
  margin-right: 16px;
}

/* file upload button hover state */
input[type="file"]::file-selector-button:hover {
  background-color: var(--vt-c-blue-soft);
}

.submit-button {
  display: block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: var(--vt-c-blue);
  color: var(--vt-c-white);
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: var(--vt-c-blue-soft);
}

.submit-button:disabled {
  background-color:var(--vt-c-grey);
  cursor: not-allowed;
}
</style>
