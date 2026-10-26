<script setup>
import { ref, onMounted } from 'vue'
import taskApi from './services/api' // 1. Impor instance Axios yang telah dibuat

// 2. State reaktif
const tasks = ref([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

const newTask = ref({
  title: '',
  description: '',
  status: 'Todo'
})

// 3. Fungsi Ambil Data (GET)
const fetchTasks = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await taskApi.getTasks()
    tasks.value = response.data // Axios otomatis mem-parsing JSON ke .data
  } catch (error) {
    errorMessage.value = 'Gagal memuat tugas dari database.'
    console.error('Error saat fetch tasks:', error)
  } finally {
    isLoading.value = false
  }
}

// 4. Fungsi Tambah Data (POST)
const addTask = async () => {
  if (!newTask.value.title.trim()) return

  isSubmitting.value = true
  try {
    await taskApi.createTask({
      title: newTask.value.title,
      description: newTask.value.description,
      status: newTask.value.status
    })

    // Reset isi form input
    newTask.value.title = ''
    newTask.value.description = ''
    newTask.value.status = 'Todo'

    // Panggil fetchTasks ulang (Refetch strategy)
    await fetchTasks()
  } catch (error) {
    alert('Gagal menyimpan tugas baru ke server.')
    console.error('Error saat create task:', error)
  } finally {
    isSubmitting.value = false
  }
}

// 5. Fungsi Update Status (PUT)
const toggleStatus = async (task) => {
  const nextStatus = {
    'Todo': 'In Progress',
    'In Progress': 'Done',
    'Done': 'Todo'
  }

  const updatedStatus = nextStatus[task.status] || 'Todo'

  try {
    await taskApi.updateTask(task.id, {
      title: task.title,
      description: task.description,
      status: updatedStatus
    })

    // Fetch ulang agar status di layar sinkron dengan DB
    await fetchTasks()
  } catch (error) {
    alert('Gagal memperbarui status tugas.')
    console.error('Error saat update task:', error)
  }
}

// 6. Fungsi Hapus Data (DELETE)
const deleteTask = async (id) => {
  if (!confirm('Apakah kamu yakin ingin menghapus tugas ini?')) return

  try {
    await taskApi.deleteTask(id)
    // Fetch ulang setelah data terhapus di backend
    await fetchTasks()
  } catch (error) {
    alert('Gagal menghapus tugas dari server.')
    console.error('Error saat delete task:', error)
  }
}

// 7. Lifecycle Hook: Ambil data otomatis saat komponen pertama kali dimuat
onMounted(() => {
  fetchTasks()
})
</script>

<template>
  <div class="min-h-screen bg-[#fcfcfc] text-gray-800 pb-16" style="font-family: Arial, Helvetica, sans-serif;">
    
    <!-- TOP NAVIGATION BAR -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-30">
      <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-8">
          <div class="flex items-center gap-2">
            <span class="text-lg font-extrabold text-[#009ee2] tracking-tight">
              Simple Task Project Tracker
            </span>
          </div>
          <nav class="hidden md:flex items-center gap-6 text-xs font-semibold text-gray-600">
            <a href="#" class="text-[#009ee2] border-b-2 border-[#009ee2] pb-5 pt-5">Workspace</a>
            <a href="#" class="hover:text-gray-900 transition">All Tasks</a>
          </nav>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center select-none" title="User Profile">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 pt-8 space-y-6">
      
      <!-- PAGE TITLE -->
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">Task Management Workspace</h1>
        <p class="text-xs text-gray-400 mt-1">Kelola dan pantau seluruh pengerjaan tugas proyek</p>
      </div>

      <!-- KONTEN UTAMA: DUA KOLOM BERGAYA KARTU -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        
        <!-- KOLOM KIRI: FORM CREATE TASK -->
        <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-xs">
          <div class="bg-[#009ee2] px-5 py-3.5 text-white font-bold text-sm tracking-wide">
            Add New Task
          </div>
          <form @submit.prevent="addTask" class="p-5 space-y-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">
                Task Title
              </label>
              <input
                v-model="newTask.title"
                type="text"
                placeholder="e.g. Slicing UI Dashboard"
                required
                class="w-full text-xs bg-white border border-gray-300 rounded-md px-3 py-2 text-gray-800 placeholder-gray-400 outline-none focus:border-[#009ee2] focus:ring-1 focus:ring-[#009ee2] transition"
              />
            </div>

            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">
                Description
              </label>
              <textarea
                v-model="newTask.description"
                rows="3"
                placeholder="Detailed objectives..."
                class="w-full text-xs bg-white border border-gray-300 rounded-md px-3 py-2 text-gray-800 placeholder-gray-400 outline-none focus:border-[#009ee2] focus:ring-1 focus:ring-[#009ee2] transition resize-none"
              ></textarea>
            </div>

            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">
                Initial Status
              </label>
              <select
                v-model="newTask.status"
                class="w-full text-xs bg-white border border-gray-300 rounded-md px-3 py-2 text-gray-700 outline-none focus:border-[#009ee2] transition"
              >
                <option value="Todo">Todo</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </select>
            </div>

            <button
              type="submit"
              :disabled="isSubmitting"
              class="w-full bg-[#009ee2] hover:bg-[#0089c4] disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-bold py-2.5 rounded-md transition shadow-xs cursor-pointer tracking-wider uppercase flex items-center justify-center gap-2"
            >
              <svg v-if="isSubmitting" class="animate-spin h-3.5 w-3.5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>{{ isSubmitting ? 'Menyimpan...' : '+ Create Task' }}</span>
            </button>
          </form>
        </div>

        <!-- KOLOM KANAN: DAFTAR TUGAS -->
        <div class="lg:col-span-2 bg-white rounded-lg border border-gray-200 overflow-hidden shadow-xs">
          <div class="bg-[#009ee2] px-5 py-3.5 text-white font-bold text-sm tracking-wide flex items-center justify-between">
            <span>Task List Display</span>
            <span class="text-xs bg-white/20 font-semibold px-2.5 py-1 rounded text-white">
              {{ tasks.length }} Tasks Total
            </span>
          </div>

          <div class="divide-y divide-gray-100">
            <!-- TAMPILAN LOADING -->
            <div v-if="isLoading" class="py-12 flex flex-col items-center justify-center text-gray-400 gap-2">
              <svg class="animate-spin h-6 w-6 text-[#009ee2]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span class="text-xs">Memuat daftar tugas...</span>
            </div>

            <!-- TAMPILAN ERROR -->
            <div v-else-if="errorMessage" class="p-6">
              <div class="bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-md text-xs flex flex-col sm:flex-row items-center justify-between gap-3">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-rose-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <line x1="12" y1="8" x2="12" y2="12" stroke-width="2"/>
                    <line x1="12" y1="16" x2="12.01" y2="16" stroke-width="2"/>
                  </svg>
                  <span>{{ errorMessage }}</span>
                </div>
                <button
                  @click="fetchTasks"
                  class="bg-rose-600 hover:bg-rose-700 text-white font-bold px-3 py-1.5 rounded transition uppercase text-[10px] cursor-pointer"
                >
                  Coba Lagi
                </button>
              </div>
            </div>

            <!-- TAMPILAN KOSONG -->
            <div v-else-if="tasks.length === 0" class="py-12 text-center text-xs text-gray-400">
              Belum ada tugas yang ditambahkan.
            </div>

            <!-- LOOPING SETIAP TUGAS -->
            <div
              v-else
              v-for="(task, index) in tasks"
              :key="task.id"
              class="p-4 hover:bg-gray-50/60 transition flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div class="space-y-1 flex-1">
                <div class="flex items-center gap-2.5">
                  <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                    #{{ String(tasks.length - index).padStart(2, '0') }}
                  </span>
                  <h3 class="text-xs font-semibold text-gray-900">
                    {{ task.title }}
                  </h3>
                </div>
                <p v-if="task.description" class="text-xs text-gray-500 line-clamp-2">
                  {{ task.description }}
                </p>
              </div>

              <!-- TOMBOL STATUS & HAPUS BERGAYA SOLID -->
              <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
                <button
                  @click="toggleStatus(task)"
                  class="text-white text-xs font-bold py-2 px-3.5 rounded-md transition shadow-xs cursor-pointer tracking-wider uppercase"
                  :class="{
                    'bg-slate-600 hover:bg-slate-700': task.status === 'Todo',
                    'bg-[#009ee2] hover:bg-[#0089c4]': task.status === 'In Progress',
                    'bg-emerald-600 hover:bg-emerald-700': task.status === 'Done'
                  }"
                  title="Klik untuk mengubah status tugas"
                >
                  {{ task.status }}
                </button>

                <button
                  @click="deleteTask(task.id)"
                  class="bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold py-2 px-3.5 rounded-md transition shadow-xs cursor-pointer tracking-wider uppercase"
                  title="Hapus tugas"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

    </main>
  </div>
</template>