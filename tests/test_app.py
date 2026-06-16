import pytest
from app import app


@pytest.fixture
def client():
    """Fixture untuk membuat test client Flask dan mereset data sebelum pengujian."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Mengimpor daftar tasks global dari app untuk mereset kondisi awal data
        from app import tasks
        tasks.clear()
        tasks.extend([
            {"id": 1, "title": "Belajar Kualitas Perangkat Lunak", "status": "Pending"},
            {"id": 2, "title": "Mengerjakan Praktikum Bab 8", "status": "Completed"}
        ])
        yield client


# ==============================================================================
# 5+ SKENARIO UJI FUNGSIONAL (HAPPY PATH & SAD PATH)
# ==============================================================================

# Skenario 1: Membuka Halaman Utama (Happy Path)
def test_index_route(client):
    """Memastikan halaman utama dapat diakses dan menampilkan komponen utama."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Task Manager System" in response.data
    assert b"Belajar Kualitas Perangkat Lunak" in response.data


# Skenario 2: Menambahkan Tugas Baru dengan Benar (Happy Path)
def test_add_task_success(client):
    """Memastikan tugas baru berhasil ditambahkan dan diarahkan kembali ke halaman utama."""
    payload = {"title": "Membaca Dokumentasi Locust"}
    response = client.post('/add', data=payload, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Membaca Dokumentasi Locust" in response.data


# Skenario 3: Gagal Menambahkan Tugas Karena Judul Kosong (Sad Path)
def test_add_task_empty_title(client):
    """Memastikan sistem menolak penambahan tugas dengan string kosong (Error 400)."""
    payload = {"title": "   "}  # Hanya berisi spasi
    response = client.post('/add', data=payload)
    
    assert response.status_code == 400
    assert b"Judul tugas tidak boleh kosong!" in response.data


# Skenario 4: Memperbarui Status Tugas Menjadi Selesai (Happy Path)
def test_update_task_success(client):
    """Memastikan status tugas dengan ID yang valid berubah menjadi 'Completed'."""
    response = client.post('/update/1', follow_redirects=True)
    assert response.status_code == 200
    
    # Memeriksa perubahan status secara langsung pada data internal aplikasi
    from app import tasks
    assert tasks[0]["status"] == "Completed"


# Skenario 5: Gagal Memperbarui Tugas Karena ID Tidak Ditemukan (Sad Path)
def test_update_task_not_found(client):
    """Memastikan sistem melempar error 404 jika ID tugas yang akan di-update fiktif."""
    response = client.post('/update/999')
    assert response.status_code == 404
    assert b"Tugas tidak ditemukan!" in response.data


# Skenario 6: Menghapus Tugas Berhasil (Happy Path)
def test_delete_task_success(client):
    """Memastikan tugas dengan ID yang valid sukses dihapus dari daftar."""
    response = client.post('/delete/2', follow_redirects=True)
    assert response.status_code == 200
    
    from app import tasks
    # Memastikan jumlah tugas berkurang menjadi 1 setelah ID 2 dihapus
    assert len(tasks) == 1


# Skenario 7: Gagal Menghapus Tugas Karena ID Tidak Ditemukan (Sad Path)
def test_delete_task_not_found(client):
    """Memastikan sistem melempar error 404 jika ID tugas yang akan dihapus fiktif."""
    response = client.post('/delete/999')
    assert response.status_code == 404
    assert b"Tugas tidak ditemukan!" in response.data


# Skenario 8: Memeriksa Endpoint API JSON (Happy Path)
def test_get_tasks_api(client):
    """Memastikan endpoint API mengembalikan data berformat JSON dengan struktur yang tepat."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 2
    assert json_data[0]["title"] == "Belajar Kualitas Perangkat Lunak"