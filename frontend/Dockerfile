FROM node:20-alpine

WORKDIR /app

# Salin file package untuk install dependensi
COPY package*.json ./
RUN npm install

# Salin seluruh kode frontend
COPY . .

# Expose port Vite dev server
EXPOSE 5173

# Jalankan Vite dengan host 0.0.0.0 agar bisa diakses dari luar container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]