import json 
import os 
from datetime import datetime

class FinanceTracer:
    """Inisiasi Untuk menambahkan Data Waktu di tambahkan otomatis"""
    def __init__(self, name, price,category):
        self.name = name
        self.price = price
        self.category = category
        self.timestamp = datetime.now().strftime("%A, %H:%M, %d-%m-%Y")
    
    def to_dict(self):
        """Mengubah data input jadi Dictionary dan manggil fungsi tambah waktu"""
        return {
            'name' : self.name,
            'price' : self.price,
            'category' : self.category,
            'timestamp' : self.timestamp
            }

class DataTransaction:
    """Inisiasi Class Utama untuk menyimpan semua fungsi tambah, edit hapus dll.."""
    def __init__ (self, FILE_DB='financetracer_db.json'):
        """Untuk memangil fungsi muat data dan menyiapkan data sementara ibarat-nya Ram"""
        self.FILE_DB = FILE_DB
        self.list_item = self.load_json()
    
    def load_json(self):
        """fungsi untuk memuat data dan membuat file baru jika belum ada"""
        if not os.path.exists(self.FILE_DB):
            return []
        try:
            with open(self.FILE_DB, 'r') as f:
                print("[📫]: Data Berhasil di Muat")
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
            
    def save_to_json(self):
        """Untuk menyimpan data secara permanen menggunakan file json ibarat-nya SSD"""
        with open(self.FILE_DB, 'w') as f:
            json.dump(self.list_item, f, indent=2)
            print("[📬]: Data Berhasil di simpan ")

    def add_to_list(self, name, price, category):
        """menambahkan list baru dan memanggil class fungsi to_dict dan langsung memanggil fungsi save_to_json"""
        FT = FinanceTracer(name, price, category)
        self.list_item.append(FT.to_dict())
        self.save_to_json()

    def show_all(self):
        """fungsi untuk melihat seluruh data yang tersimpan"""
        if not self.list_item:
            print ("\n[📭]: List Masih Kosong")
            return
        print("\n" + "—"*15 + " My Finance Tracer" + "—"*15)
        for index, entry in enumerate(self.list_item):
            print(f"[{index}]) {entry['timestamp']}\n {entry['name']} {entry['price']} {entry['category']}" )
            print("-" * 47)

    def edit_db(self):
        """fungsi untuk mengubah data yang tersimpan menggunakan if agar saat di kosongkan data tidak di ubah"""
        self.show_all()
        if not self.list_item:
            print("[📭]Masih kosong Kosong")
        try:
            target = int(input("Masukan Nomer Data yang akan di ubah: "))
            entry = self.list_item[target]
            print(f"{entry['name']} {entry['price']} {entry['category']}")
            print ("Kosongkan Jika tidak ingin di ubah Tekan [Enter]")
            new_name = input("masukan nama baru: ").lower()
            new_price = input("masukan harga baru: ")
            new_category = input("masukan kategori baru (makanan/minuman/lainya): ")
            if new_name:
                entry['name'] = new_name
            if new_price.isdigit():
                entry['price'] = new_price
            if new_category:
                entry['category'] = new_category
            self.save_to_json()
            print("[📬]: Data Berhasil Di Perbahrui ")
        except (IndexError, ValueError):
            print("[Error] Nomer Tidak Valid")

    def delete_data(self):
        """fungsi untuk menghapus satu entry data yang tersimpan"""
        self.show_all()
        if not self.list_item:
            return
        try:
            target = int(input("Masukan Nomer Index: "))
            confirm = input("Anda Yakin [y/n]: ")
            if confirm == 'y':
                removed = self.list_item.pop(target)
                self.save_to_json()
                print(f"[📭]: Berhasil menghapus: {removed['name']}")
            else:
                print("[📬]: Penghapusan dibatalkan.")
        except (IndexError, ValueError):
            print("[📭]: Error: Nomor index tidak valid!")
        except Exception as e:
            print(f"Error Terjadi: {e}")
    
    def calculate_total(self):
        """Menghitung semua data harga yang tersimpan menggunakan int untuk memaksa str jadi int"""
        if not self.list_item:
            print("[📭]: Data masih kosong.")
            return
        try:
            total = 0
            for entry in self.list_item:
                total += int(entry['price'])
            print("\n" + "="*30)
            print(f"TOTAL PENGELUARAN: Rp {total:,}")
            print("="*30)
        except Exception as e:
            print (e)

    def search_by_name(self):
        find = input("[🔎]: Cari Nama Barang: ").lower()
        found_items = [i for i in self.list_item if find in i['name'].lower()]
        if found_items:
            print(f"\n[📬]: Hasil Pencarian '{find}':")
            for idx, item in enumerate(found_items):
                print(f"{idx}. {item['name']} - Rp {item['price']}")
        else:
            print(f"[🗳]: Barang '{find}' tidak di temukan.")


    def sort_by_price(self, expensive_first=True):
        """mengurutkan data sesuai harga yang paling mahal"""
        if not self.list_item:
            print("[📭] Data kosong, nggak ada yang bisa diurutkan.")
            return
        self.list_item.sort(key=lambda item: int(item['price']), reverse=expensive_first)
        print(f"\n✅ Data berhasil diurutkan berdasarkan harga {'Termahal' if expensive_first else 'Termurah'}!")
        self.save_to_json()
        self.show_all()

    def get_summary(self):
        """fungsi Untuk metangkum semua dari perkategori sampai menjumlahkan semuanya"""
        if not self.list_item:
            print("[📭]: Belum ada data yang tersedia")
            return 
        total_all = 0
        categories = {}
        for item in self.list_item:
            price =int(item['price'])
            category = item.get('category', 'Lainya')
            total_all += price
            if category in categories:
                categories[category] += price 
            else:
                categories[category] = price
        print ("—"*30)
        print (f"[🧾]: Total Pengeluaran\n       Rp{total_all:,}")
        print ("—"*30)
        print ("[🧾]: Detail Per-Category: ")
        for cat, total in categories.items():
            print (f" ≥ {cat.capitalize()}: Rp{total:,}")
        expensive = max(self.list_item, key=lambda x: int(x['price']))
        print ("—"*30)
        print (f"[🧾]:Expensive\n {expensive['name']}. ≥ Rp {int(expensive['price']):,}")
        print ("—"*30)
        
    def clear_db(self):
        """fungsi untuk menghapus semua data yang tersimpan"""
        list.clear(self.list_item)
        self.save_to_json()

if __name__ == "__main__":
    DT = DataTransaction()
    while True:
        print ("—————Finance Tracer—————")
        print(" 1. Tambah\n", "2. Edit\n","3. Hapus\n", "4. Hitung\n","5. Cari\n", "6. Lihat Semua\n", "7. Rangkum semua\n", "8. Hapus semua\n", "9. Keluar\n")
        pilih = input("[⚙]: [Masukan Pilihan]: ").strip()
        if pilih == '1':
            name = input("Masukan Nama Barang: ")
            price = input("Masukan Harga Barang: ")
            while not price.isdigit():
                print("[🗳]: Masukan hanya angka")
                price = input("Masukan Harga Barang: ")
            category = input("Masukan Category: ")
            DT.add_to_list(name, price, category)
        elif pilih == '2':
            DT.edit_db()
        elif pilih == '3':
            DT.delete_data()
        elif pilih == '4':
            DT.calculate_total()
        elif pilih == '5':
            DT.search_by_name()
        elif pilih == '6':
            DT.show_all()
        elif pilih == '7':
            DT.get_summary()
        elif pilih == '8':
            DT.clear_db()
        elif pilih == '9':
            print("GoodBye")
            break
        else:
            print("[⚙]: Input Tidak Valid")