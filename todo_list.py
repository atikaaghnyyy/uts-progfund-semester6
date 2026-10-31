# ============================================================
# UJIAN AKHIR SEMESTER - FUNDAMENTAL PROGRAMMING (PYTHON)
# Studi Kasus : To-Do List Application 
# Nama        : Atika Nur Aghny
# NIM         : 24120300020
# ============================================================

import csv

DATA_FILE = "tasks.csv"
PRIORITY_LEVELS = ("Tinggi", "Sedang", "Rendah")

MENU_OPTIONS = (
    "Lihat Semua Task",
    "Tambah Task",
    "Ubah Task",
    "Hapus Task",
    "Tandai Task Selesai",
    "Cari Task",
    "Ringkasan Progres",
    "Keluar",
)

class Task:
    title: str
    priority: str
    done: bool

    def __init__(self, title: str, priority: str, done: bool = False) -> None:
        self.title = title
        self.priority = priority
        self.done = done

    def mark_done(self) -> None:
        self.done = True

    def matches(self, keyword: str) -> bool:
        keyword = keyword.strip().lower()
        return keyword in self.title.lower()

    def status_symbol(self) -> str:
        if self.done:
            return "[v]"
        return "[ ]"

    def to_row(self) -> list:
        return [self.title, self.priority, str(self.done)]

class TaskManager:
    filename: str
    tasks: list

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.tasks = []
        self.load_from_csv()

    def load_from_csv(self) -> None:
        try:
            with open(self.filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)              # lewati baris header
                for row in reader:
                    if len(row) < 3:
                        continue                # lewati baris rusak
                    title = row[0].strip()
                    priority = row[1].strip()
                    done = row[2].strip().lower() == "true"
                    self.tasks.append(Task(title, priority, done))
        except FileNotFoundError:
            self.tasks = []

    def save_to_csv(self) -> None:
        try:
            with open(self.filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "priority", "done"])
                for task in self.tasks:
                    writer.writerow(task.to_row())
        except OSError:
            print("Gagal menyimpan data ke file.")

    def title_exists(self, title: str) -> bool:
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return True
        return False

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save_to_csv()

    def remove_task(self, index: int) -> Task:
        removed = self.tasks.pop(index)
        self.save_to_csv()
        return removed

    def count_done(self) -> int:
        done = 0
        for task in self.tasks:
            if task.done:
                done = done + 1
        return done

def clean_text(text: str) -> str:
    return " ".join(text.split())

def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Input harus berupa angka! Coba lagi.")

def display_menu() -> None:
    print()
    print("=============================================")
    print("            TO-DO LIST APPLICATION           ")
    print("=============================================")
    number = 1
    for option in MENU_OPTIONS:
        print(f"{number}. {option}")
        number = number + 1
    print("=============================================")

def display_tasks(manager: TaskManager, only_pending: bool = False) -> None:
    print()
    print("------------- DAFTAR TASK -------------")

    if len(manager.tasks) == 0:
        print("Belum ada task. Silakan tambah task terlebih dahulu.")
        print("---------------------------------------")
        return

    number = 1
    for task in manager.tasks:
        if only_pending and task.done:
            number = number + 1
            continue
        print(f"{number}. {task.status_symbol()} {task.title} (Prioritas: {task.priority})")
        number = number + 1

    print("---------------------------------------")
    print("Keterangan: [v] = selesai, [ ] = belum selesai")

def choose_priority() -> str:
    while True:
        print("Pilih prioritas:")
        for i in range(len(PRIORITY_LEVELS)):
            print(f"  {i + 1}. {PRIORITY_LEVELS[i]}")

        choice = read_int("Masukkan nomor prioritas: ")
        if 1 <= choice <= len(PRIORITY_LEVELS):
            return PRIORITY_LEVELS[choice - 1]
        else:
            print(f"Prioritas tidak valid! Pilih angka 1 sampai {len(PRIORITY_LEVELS)}")

def get_task_number(manager: TaskManager, action_name: str) -> int:
    while True:
        number = read_int(f"Masukkan nomor task yang ingin {action_name} (0 = batal): ")
        if number == 0:
            print("Aksi dibatalkan.")
            return -1
        elif 1 <= number <= len(manager.tasks):
            return number - 1
        else:
            print("Task dengan nomor tersebut tidak ditemukan! Coba lagi.")

def add_task(manager: TaskManager) -> None:
    print()
    print("------------- TAMBAH TASK -------------")
    title = clean_text(input("Masukkan nama task: "))

    if title == "":
        print("Nama task tidak boleh kosong!")
        return
    if manager.title_exists(title):
        print(f"Task '{title}' sudah ada! Gunakan nama lain.")
        return

    priority = choose_priority()
    manager.add_task(Task(title, priority))
    print(f"Task '{title}' berhasil ditambahkan dengan prioritas {priority}")


def update_task(manager: TaskManager) -> None:
    if len(manager.tasks) == 0:
        print()
        print("Belum ada task yang bisa diubah.")
        return

    display_tasks(manager)
    index = get_task_number(manager, "diubah")
    if index == -1:
        return

    task = manager.tasks[index]
    print()
    print(f"Nama task saat ini : {task.title}")
    print(f"Prioritas saat ini : {task.priority}")

    new_title = clean_text(input("Nama task baru (tekan Enter jika tidak diubah): "))
    if new_title == "":
        new_title = task.title
    elif new_title.lower() != task.title.lower() and manager.title_exists(new_title):
        print(f"Task '{new_title}' sudah ada! Perubahan dibatalkan.")
        return

    while True:
        answer = input("Ubah prioritas? (y/n): ").strip().lower()
        if answer == "y":
            task.priority = choose_priority()
            break
        elif answer == "n":
            break
        else:
            print("Jawaban tidak valid! Ketik y atau n.")

    task.title = new_title
    manager.save_to_csv()
    print(f"Task berhasil diubah menjadi: {task.title} | Prioritas: {task.priority}")


def delete_task(manager: TaskManager) -> None:
    if len(manager.tasks) == 0:
        print()
        print("Belum ada task yang bisa dihapus.")
        return

    display_tasks(manager)
    index = get_task_number(manager, "dihapus")
    if index == -1:
        return

    title = manager.tasks[index].title
    while True:
        confirm = input(f"Yakin ingin menghapus task '{title}'? (y/n): ").strip().lower()
        if confirm == "y":
            removed = manager.remove_task(index)
            print(f"Task '{removed.title}' berhasil dihapus.")
            break
        elif confirm == "n":
            print("Penghapusan dibatalkan.")
            break
        else:
            print("Jawaban tidak valid! Ketik y atau n.")


def mark_task_done(manager: TaskManager) -> None:
    if len(manager.tasks) == 0:
        print()
        print("Belum ada task.")
        return

    if manager.count_done() == len(manager.tasks):
        print()
        print("Semua task sudah selesai. Tidak ada yang perlu ditandai.")
        return

    print()
    print("Task yang belum selesai:")
    display_tasks(manager, only_pending=True)
    index = get_task_number(manager, "ditandai selesai")
    if index == -1:
        return

    task = manager.tasks[index]
    if task.done:
        print(f"Task '{task.title}' sudah berstatus selesai sebelumnya.")
    else:
        task.mark_done()
        manager.save_to_csv()
        print(f"Task '{task.title}' ditandai SELESAI.")

def search_task(manager: TaskManager) -> None:
    print()
    print("------------- CARI TASK -------------")
    if len(manager.tasks) == 0:
        print("Belum ada task untuk dicari.")
        return

    keyword = clean_text(input("Masukkan kata kunci: "))
    if keyword == "":
        print("Kata kunci tidak boleh kosong!")
        return

    found = 0
    number = 1
    for task in manager.tasks:
        if task.matches(keyword):
            print(f"{number}. {task.status_symbol()} {task.title} (Prioritas: {task.priority})")
            found = found + 1
        number = number + 1

    if found == 0:
        print(f"Tidak ada task yang mengandung kata '{keyword}'.")
    else:
        print(f"Ditemukan {found} task.")


def display_summary(manager: TaskManager) -> None:
    total = len(manager.tasks)
    done = manager.count_done()
    pending = total - done

    if total > 0:
        percentage = round(done / total * 100, 1)
    else:
        percentage = 0.0

    print()
    print("----------- RINGKASAN PROGRES -----------")
    print(f"Total task         : {total}")
    print(f"Task selesai       : {done}")
    print(f"Task belum selesai : {pending}")
    print(f"Progres            : {percentage} %")

    priority_count = {}
    for level in PRIORITY_LEVELS:
        priority_count[level] = 0
    for task in manager.tasks:
        if not task.done:
            priority_count[task.priority] = priority_count[task.priority] + 1

    print()
    print("Task belum selesai per prioritas:")
    for level, count in priority_count.items():
        print(f"  - {level} : {count} task")

    print()
    if total == 0:
        print("Belum ada task. Yuk mulai tambahkan task!")
    elif percentage == 100:
        print("Luar biasa! Semua task sudah selesai.")
    elif percentage >= 50:
        print("Bagus! Setengah atau lebih task sudah selesai.")
    elif percentage > 0:
        print("Terus semangat, masih ada task yang perlu diselesaikan.")
    else:
        print("Belum ada task yang selesai. Ayo mulai kerjakan!")
    print("-----------------------------------------")

def main() -> None:
    # membuat object dari class TaskManager (Task D)
    manager = TaskManager(DATA_FILE)

    print("Selamat datang di To-Do List Application!")
    if len(manager.tasks) > 0:
        print(f"Memuat {len(manager.tasks)} task dari {DATA_FILE}")

    user_name = clean_text(input("Masukkan nama Anda: "))
    if user_name == "":
        user_name = "User"
    print(f"Halo, {user_name}! Ayo atur task kamu hari ini.")

    while True:
        display_menu()
        choice = read_int("Pilih menu (1-8): ")

        if choice == 1:
            display_tasks(manager)
        elif choice == 2:
            add_task(manager)
        elif choice == 3:
            update_task(manager)
        elif choice == 4:
            delete_task(manager)
        elif choice == 5:
            mark_task_done(manager)
        elif choice == 6:
            search_task(manager)
        elif choice == 7:
            display_summary(manager)
        elif choice == 8:
            done = manager.count_done()
            total = len(manager.tasks)
            print()
            print(f"Terima kasih, {user_name}!")
            print(f"Hari ini kamu menyelesaikan {done} dari {total} task.")
            print(f"Data tersimpan di {DATA_FILE}. Sampai jumpa!")
            break
        else:
            print("Pilihan menu tidak valid! Masukkan angka 1 sampai 8.")
            continue

        input("Tekan Enter untuk kembali ke menu...")

try:
    main()
except KeyboardInterrupt:
    print()
    print("Program dihentikan oleh pengguna.")