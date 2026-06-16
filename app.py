from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# In-memory database (sementara) untuk menyimpan data tugas
tasks = [
    {"id": 1, "title": "Belajar Kualitas Perangkat Lunak", "status": "Pending"},
    {"id": 2, "title": "Mengerjakan Praktikum Bab 8", "status": "Completed"}
]


@app.route("/")
def index():
    """Menampilkan halaman utama beserta daftar tugas."""
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    """Menambahkan tugas baru ke dalam daftar."""
    title = request.form.get("title")
    
    # Skenario Gagal: Judul kosong atau hanya berisi spasi
    if not title or title.strip() == "":
        return "Judul tugas tidak boleh kosong!", 400

    # Membuat ID baru secara otomatis
    new_id = max([task["id"] for task in tasks]) + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": title.strip(),
        "status": "Pending"
    }
    tasks.append(new_task)
    return redirect("/")


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    """Mengubah status tugas menjadi 'Completed'."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            return redirect("/")
            
    # Skenario Gagal: ID tugas tidak ditemukan
    return "Tugas tidak ditemukan!", 404


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Menghapus tugas dari daftar berdasarkan ID."""
    global tasks
    task_exists = any(task["id"] == task_id for task in tasks)
    
    # Skenario Gagal: ID tugas tidak ditemukan
    if not task_exists:
        return "Tugas tidak ditemukan!", 404

    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect("/")


@app.route("/api/tasks", methods=["GET"])
def get_tasks_api():
    """Endpoint khusus API JSON untuk mempermudah load testing dengan Locust."""
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)