import axios from 'axios'

// 1. Inisialisasi Axios instance dengan base URL backend FastAPI
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// 2. Kumpulan fungsi API untuk komunikasi dengan endpoint /tasks
const taskApi = {
  // GET /tasks: Mengambil seluruh daftar tugas
  getTasks: () => apiClient.get('/tasks'),

  // POST /tasks: Menambahkan tugas baru
  createTask: (taskData) => apiClient.post('/tasks', taskData),

  // PUT /tasks/{id}: Memperbarui data atau status tugas berdasarkan ID
  updateTask: (id, taskData) => apiClient.put(`/tasks/${id}`, taskData),

  // DELETE /tasks/{id}: Menghapus tugas berdasarkan ID
  deleteTask: (id) => apiClient.delete(`/tasks/${id}`),

  // Akses langsung ke apiClient jika dibutuhkan
  client: apiClient,
}

export { apiClient }
export default taskApi
