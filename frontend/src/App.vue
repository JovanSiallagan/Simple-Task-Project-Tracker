<script setup>
import { ref } from 'vue'

// 1. DATA REAKTIF FORM INPUT
const newTask = ref({
  title: '',
  description: '',
  status: 'Todo'
})

// 2. DATA DUMMY TUGAS
const tasks = ref([
  {
    id: 1,
    title: 'Setup Database PostgreSQL & Docker',
    description: 'Konfigurasi docker-compose.yml dengan environment variables port 5433.',
    status: 'Done'
  },
  {
    id: 2,
    title: 'Implementasi CRUD REST API',
    description: 'Endpoint FastAPI untuk Create, Read, Update, Delete data tasks.',
    status: 'In Progress'
  },
  {
    id: 3,
    title: 'Integrasi Frontend Vue 3',
    description: 'Slicing antarmuka data table dan menyambungkan axios HTTP client.',
    status: 'Todo'
  }
])

// 3. FUNGSI MENAMBAH TUGAS (Create)
const addTask = () => {
  if (!newTask.value.title.trim()) return

  tasks.value.unshift({
    id: Date.now(),
    title: newTask.value.title,
    description: newTask.value.description,
    status: newTask.value.status
  })

  // Reset form
  newTask.value.title = ''
  newTask.value.description = ''
  newTask.value.status = 'Todo'
}

// 4. FUNGSI GANTI STATUS (Toggle)
const toggleStatus = (task) => {
  const flow = {
    'Todo': 'In Progress',
    'In Progress': 'Done',
    'Done': 'Todo'
  }
  task.status = flow[task.status] || 'Todo'
}

// 5. FUNGSI HAPUS TUGAS (Delete)
const deleteTask = (id) => {
  tasks.value = tasks.value.filter(t => t.id !== id)
}
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
          <span class="text-xs bg-gray-100 text-gray-600 font-semibold px-3 py-1.5 rounded-md border border-gray-200">
            {{ tasks.length }} Tasks Total
          </span>
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
              class="w-full bg-[#009ee2] hover:bg-[#0089c4] text-white text-xs font-bold py-2.5 rounded-md transition shadow-xs cursor-pointer tracking-wider uppercase"
            >
              + Create Task
            </button>
          </form>
        </div>

        <!-- KOLOM KANAN: DAFTAR TUGAS -->
        <div class="lg:col-span-2 bg-white rounded-lg border border-gray-200 overflow-hidden shadow-xs">
          <div class="bg-[#009ee2] px-5 py-3.5 text-white font-bold text-sm tracking-wide flex items-center justify-between">
            <span>Task Deliverables & Execution</span>
            <span class="text-xs bg-white/20 font-semibold px-2 py-0.5 rounded text-white">Active</span>
          </div>

          <div class="divide-y divide-gray-100">
            <!-- TAMPILAN KOSONG -->
            <div v-if="tasks.length === 0" class="py-12 text-center text-xs text-gray-400">
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
                    #{{ String(index + 1).padStart(2, '0') }}
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