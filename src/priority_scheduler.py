"""
Modul: Priority Scheduling and Aging Simulation
Projek: OS-POPBL-Group1-RunnerTracking
Penerangan: Fail ini mengandungi logik penjadualan keutamaan (priority scheduling) 
            berserta mekanisma aging untuk memastikan tugas yang menunggu lama 
            mendapat keutamaan secara beransur-ansur.
"""

class Task:
    def __init__(self, task_id, priority, burst_time):
        self.task_id = task_id          # ID Unik untuk setiap tugas / proses
        self.priority = priority          # Tahap keutamaan (Nombor lebih tinggi = Keutamaan lebih tinggi)
        self.burst_time = burst_time      # Masa pemprosesan yang diperlukan
        self.waiting_time = 0             # Masa menunggu dalam barisan

def priority_scheduling_with_aging(tasks):
    print("==================================================")
    print("      SIMULASI PRIORITY SCHEDULING & AGAGING      ")
    print("==================================================")
    
    execution_step = 1
    
    # Teruskan gelung selagi masih ada tugas di dalam senarai
    while tasks:
        print(f"\n--- Pusingan (Step) {execution_step} ---")
        
        # 1. Susun senarai tugas:
        # - Keutamaan (priority) tertinggi diutamakan dulu (reverse=True)
        # - Jika priority sama, pilih tugas yang mempunyai masa menunggu (waiting_time) paling lama
        tasks.sort(key=lambda x: (x.priority, x.waiting_time), reverse=True)
        
        # Paparkan status barisan semasa
        print("Status Barisan Semasa (Queue):")
        for t in tasks:
            print(f" -> Task ID: {t.task_id} | Priority: {t.priority} | Waiting Time: {t.waiting_time}")

        # 2. Ambil tugas teratas untuk dilaksana
        current_task = tasks.pop(0)
        print(f"\n[EXECUTION] Melaksanakan **Task {current_task.task_id}** "
              f"(Priority Asal: {current_task.priority}, Masa Menunggu: {current_task.waiting_time})")
        
        # 3. Mekanisme Aging untuk tugas lain yang masih tinggal dalam barisan
        for t in tasks:
            t.waiting_time += 1  # Tambah masa menunggu untuk tugas yang belum diproses
            
            # Jika masa menunggu mencapai ambang (threshold) tertentu, cth: >= 2 pusingan
            if t.waiting_time >= 2:
                t.priority += 1  # Tingkatkan tahap priority (Aging)
                print(f"   -> [AGING ALERT] Task {t.task_id} terbiar terlalu lama. Priority dinaikkan ke **{t.priority}**!")
                t.waiting_time = 0  # Reset masa menunggu selepas kenaikan priority
        
        execution_step += 1

    print("\n==================================================")
    print("      Semua tugas telah berjaya diselesaikan!     ")
    print("==================================================")

# Blok utama untuk menguji simulasi
if __name__ == "__main__":
    # Contoh data awal tugas (Anda boleh ubah nilai priority & burst time mengikut keperluan)
    initial_tasks = [
        Task(task_id=101, priority=1, burst_time=5),
        Task(task_id=102, priority=3, burst_time=3),
        Task(task_id=103, priority=2, burst_time=4)
    ]
    
    priority_scheduling_with_aging(initial_tasks)
