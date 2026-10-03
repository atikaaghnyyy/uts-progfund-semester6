# ============================================================
# UJIAN TENGAH SEMESTER - FUNDAMENTAL PROGRAMMING (PYTHON)
# Studi Kasus : To-Do List Application
# Nama        : Atika Nur Aghny
# NIM         : 24120300020
# ============================================================

priority_levels = ("Tinggi", "Sedang", "Rendah")

menu_options = (
    "Lihat Semua Task",
    "Tambah Task",
    "Ubah Task",
    "Hapus Task",
    "Tandai Task Selesai",
    "Ringkasan Progres",
    "Keluar",
)

def display_menu():
    print()
    print("=============================================")
    print("            TO-DO LIST APPLICATION           ")
    print("=============================================")
    number = 1
    for option in menu_options:
        print(str(number) + ". " + option)
        number = number + 1
    print("=============================================")


def display_tasks(tasks, only_pending=False):
    print()
    print("------------- DAFTAR TASK -------------")

    if len(tasks) == 0:
        print("Belum ada task. Silakan tambah task terlebih dahulu.")
        return

    number = 1
    for task in tasks:
        if only_pending and task["done"]:
            number = number + 1
            continue

        if task["done"]:
            status = "[v]"
        else:
            status = "[ ]"

        print(str(number) + ". " + status + " " + task["title"]
              + " (Prioritas: " + task["priority"] + ")")
        number = number + 1

    print("---------------------------------------")
    print("Keterangan: [v] = selesai, [ ] = belum selesai")

def choose_priority():
    valid_choices = []
    for i in range(len(priority_levels)):
        valid_choices.append(str(i + 1))

    while True:
        print("Pilih prioritas:")
        for i in range(len(priority_levels)):
            print("  " + str(i + 1) + ". " + priority_levels[i])

        choice = input("Masukkan nomor prioritas: ")

        if choice in valid_choices:
            index = int(choice) - 1          # type conversion str -> int
            return priority_levels[index]
        else:
            print("Prioritas tidak valid! Pilih angka 1 sampai", len(priority_levels))

def get_task_number(tasks, action_name):
    valid_numbers = []
    for i in range(1, len(tasks) + 1):
        valid_numbers.append(str(i))

    while True:
        number = input("Masukkan nomor task yang ingin " + action_name + " (0 = batal): ")

        if number == "0":
            print("Aksi dibatalkan.")
            return -1
        elif number in valid_numbers:
            return int(number) - 1
        else:
            print("Task dengan nomor tersebut tidak ditemukan! Coba lagi.")

def add_task(tasks, task_titles):
    print()
    print("------------- TAMBAH TASK -------------")
    title = input("Masukkan nama task: ")

    if title == "":
        print("Nama task tidak boleh kosong!")
        return

    if title in task_titles:
        print("Task '" + title + "' sudah ada! Gunakan nama lain.")
        return

    priority = choose_priority()

    new_task = {
        "title": title,
        "priority": priority,
        "done": False,
    }
    tasks.append(new_task)
    task_titles.add(title)

    print("Task '" + title + "' berhasil ditambahkan dengan prioritas", priority)

def update_task(tasks, task_titles):
    if len(tasks) == 0:
        print()
        print("Belum ada task yang bisa diubah.")
        return

    display_tasks(tasks)
    index = get_task_number(tasks, "diubah")
    if index == -1:
        return

    task = tasks[index]
    old_title = task["title"]
    print()
    print("Nama task saat ini     :", task["title"])
    print("Prioritas saat ini     :", task["priority"])

    new_title = input("Nama task baru (tekan Enter jika tidak diubah): ")
    if new_title == "":
        new_title = old_title
    elif new_title != old_title and new_title in task_titles:
        print("Task '" + new_title + "' sudah ada! Perubahan dibatalkan.")
        return

    while True:
        answer = input("Ubah prioritas? (y/n): ")
        if answer == "y" or answer == "Y":
            task["priority"] = choose_priority()
            break
        elif answer == "n" or answer == "N":
            break
        else:
            print("Jawaban tidak valid! Ketik y atau n.")

    task_titles.discard(old_title)
    task_titles.add(new_title)
    task["title"] = new_title

    print("Task berhasil diubah menjadi:", task["title"], "| Prioritas:", task["priority"])

def delete_task(tasks, task_titles):
    if len(tasks) == 0:
        print()
        print("Belum ada task yang bisa dihapus.")
        return

    display_tasks(tasks)
    index = get_task_number(tasks, "dihapus")
    if index == -1:
        return

    title = tasks[index]["title"]

    while True:
        confirm = input("Yakin ingin menghapus task '" + title + "'? (y/n): ")
        if confirm == "y" or confirm == "Y":
            removed_task = tasks.pop(index)
            task_titles.discard(removed_task["title"])
            print("Task '" + removed_task["title"] + "' berhasil dihapus.")
            break
        elif confirm == "n" or confirm == "N":
            print("Penghapusan dibatalkan.")
            break
        else:
            print("Jawaban tidak valid! Ketik y atau n.")

def mark_task_done(tasks):
    if len(tasks) == 0:
        print()
        print("Belum ada task.")
        return

    total, done, pending, percentage = calculate_progress(tasks)
    if pending == 0:
        print()
        print("Semua task sudah selesai. Tidak ada yang perlu ditandai.")
        return

    print()
    print("Task yang belum selesai:")
    display_tasks(tasks, only_pending=True)
    index = get_task_number(tasks, "ditandai selesai")
    if index == -1:
        return

    if tasks[index]["done"]:
        print("Task '" + tasks[index]["title"] + "' sudah berstatus selesai sebelumnya.")
    else:
        tasks[index]["done"] = True
        print("Task '" + tasks[index]["title"] + "' ditandai SELESAI.")

def calculate_progress(tasks):
    total = len(tasks)
    done = 0
    for task in tasks:
        if task["done"]:
            done = done + 1

    pending = total - done

    if total > 0:
        percentage = done / total * 100
    else:
        percentage = 0.0

    return total, done, pending, round(percentage, 1)

def display_summary(tasks):
    total, done, pending, percentage = calculate_progress(tasks)

    print()
    print("----------- RINGKASAN PROGRES -----------")
    print("Total task         :", total)
    print("Task selesai       :", done)
    print("Task belum selesai :", pending)
    print("Progres            :", percentage, "%")

    priority_count = {}
    for level in priority_levels:
        priority_count[level] = 0

    for task in tasks:
        if not task["done"]:
            priority_count[task["priority"]] = priority_count[task["priority"]] + 1

    print()
    print("Task belum selesai per prioritas:")
    for level, count in priority_count.items():
        print("  -", level, ":", count, "task")

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

def main():
    tasks = []              # list berisi dictionary task
    task_titles = set()     # set berisi judul task (agar unik)

    print("Selamat datang di To-Do List Application!")
    user_name = input("Masukkan nama Anda: ")
    if user_name == "":
        user_name = "User"
    print("Halo,", user_name + "! Ayo atur task kamu hari ini.")

    while True:
        display_menu()
        choice = input("Pilih menu (1-7): ")

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks, task_titles)
        elif choice == "3":
            update_task(tasks, task_titles)
        elif choice == "4":
            delete_task(tasks, task_titles)
        elif choice == "5":
            mark_task_done(tasks)
        elif choice == "6":
            display_summary(tasks)
        elif choice == "7":
            total, done, pending, percentage = calculate_progress(tasks)
            print()
            print("Terima kasih,", user_name + "!")
            print("Hari ini kamu menyelesaikan", done, "dari", total, "task.")
            print("Program selesai.")
            break
        else:
            print("Pilihan menu tidak valid! Masukkan angka 1 sampai 7.")
            continue

        input("Tekan Enter untuk kembali ke menu...")

main()
