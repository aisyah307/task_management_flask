from locust import HttpUser, task, between

class TaskManagerUser(HttpUser):
    # Simulasi waktu tunggu pengguna antara 1 sampai 3 detik setelah setiap aksi
    wait_time = between(1, 3)

    @task(2)
    def view_homepage(self):
        """Menyimulasikan pengguna yang membuka halaman utama Task Manager."""
        self.client.get("/")

    @task(1)
    def view_tasks_api(self):
        """Menyimulasikan integrasi sistem atau fetch data JSON dari endpoint API."""
        self.client.get("/api/tasks")
        