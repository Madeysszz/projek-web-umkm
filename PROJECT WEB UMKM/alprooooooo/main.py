from menu import tampilkan_menu
from models.pegawai import Pegawai
from models.jabatan import Jabatan
from models.departemen import Departemen
from models.gaji import Gaji
from adts.stack_adt import StackAbsen
from config.db_config import connect_db
from utils.exceptions import *

# Default data pegawai dari database
def load_daftar_pekerja(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pegawai")
    hasil = cursor.fetchall()
    daftar_pekerja = []
    for row in hasil:
        daftar_pekerja.append(Pegawai(*row))
    return daftar_pekerja

def tambah_pegawai(db):
    try:
        id_pegawai = int(input("Masukkan ID Pegawai: "))
        nama = input("Masukkan Nama: ")
        umur = int(input("Masukkan Umur: "))
        jk = input("Masukkan Jenis Kelamin (L/P): ").upper()
        if jk not in ['L', 'P']:
            raise InvalidInputError("Jenis kelamin harus L atau P.")
        alamat = input("Masukkan Alamat: ")

        cursor = db.cursor()

        # Menampilkan daftar jabatan
        cursor.execute("SELECT * FROM jabatan")
        jabatan_list = cursor.fetchall()
        print("\nDAFTAR JABATAN:")
        for j in jabatan_list:
            print(f"{j[0]}. {j[1]}")
        id_jabatan = int(input("Pilih ID Jabatan: "))

        # Menampilkan daftar departemen
        cursor.execute("SELECT * FROM departemen")
        dept_list = cursor.fetchall()
        print("\nDAFTAR DEPARTEMEN:")
        for d in dept_list:
            print(f"{d[0]}. {d[1]}")
        id_departemen = int(input("Pilih ID Departemen: "))

        gaji_pokok = float(input("Gaji Pokok: "))
        tunjangan = float(input("Tunjangan: "))
        total_gaji = gaji_pokok + tunjangan

        # Simpan ke database
        sql_pegawai = """INSERT INTO pegawai (id_pegawai, nama, umur, jenis_kelamin, alamat)
                         VALUES (%s, %s, %s, %s, %s)"""
        val_pegawai = (id_pegawai, nama, umur, jk, alamat)
        cursor.execute(sql_pegawai, val_pegawai)

        sql_gaji = """INSERT INTO gaji (id_pegawai, gaji_pokok, tunjangan, total_gaji)
                      VALUES (%s, %s, %s, %s)"""
        val_gaji = (id_pegawai, gaji_pokok, tunjangan, total_gaji)
        cursor.execute(sql_gaji, val_gaji)

        db.commit()
        print("Pegawai berhasil ditambahkan beserta gaji.")

    except ValueError:
        print("Input harus berupa angka yang valid.")
    except InvalidInputError as e:
        print(e)

def hapus_pegawai(db):
    try:
        id_pegawai = int(input("Masukkan ID Pegawai yang ingin dihapus: "))
        cursor = db.cursor()

        # Hapus dulu dari tabel gaji
        sql_gaji = "DELETE FROM gaji WHERE id_pegawai = %s"
        val_gaji = (id_pegawai,)
        cursor.execute(sql_gaji, val_gaji)

        # Lalu hapus dari absensi
        sql_absensi = "DELETE FROM absensi WHERE id_pegawai = %s"
        val_absensi = (id_pegawai,)
        cursor.execute(sql_absensi, val_absensi)

        # Setelah itu baru hapus dari pegawai
        sql_pegawai = "DELETE FROM pegawai WHERE id_pegawai = %s"
        val_pegawai = (id_pegawai,)
        cursor.execute(sql_pegawai, val_pegawai)

        db.commit()
        if cursor.rowcount == 0:
            raise DataNotFoundError("Data pegawai tidak ditemukan atau sudah dihapus.")
        print("Pegawai dan data terkait berhasil dihapus.")
        
    except ValueError:
        print("Input harus berupa angka.")
    except DataNotFoundError as e:
        print(e)

def update_pegawai(db):
    try:
        id_pegawai = int(input("Masukkan ID Pegawai yang ingin diupdate: "))
        cursor = db.cursor()

        # Cek apakah data pegawai ada
        sql_check = "SELECT * FROM pegawai WHERE id_pegawai = %s"
        cursor.execute(sql_check, (id_pegawai,))
        pegawai = cursor.fetchone()
        if not pegawai:
            raise DataNotFoundError("Data pegawai tidak ditemukan.")

        # Ambil data gaji terkait
        sql_gaji = "SELECT gaji_pokok, tunjangan FROM gaji WHERE id_pegawai = %s"
        cursor.execute(sql_gaji, (id_pegawai,))
        gaji_data = cursor.fetchone()

        print("\nData Pegawai Saat Ini:")
        print(f"ID Pegawai: {pegawai[0]}")
        print(f"Nama: {pegawai[1]}")
        print(f"Umur: {pegawai[2]}")
        print(f"Jenis Kelamin: {pegawai[3]}")
        print(f"Alamat: {pegawai[4]}")

        if gaji_data:
            print(f"Gaji Pokok: Rp{gaji_data[0]:,.2f}")
            print(f"Tunjangan: Rp{gaji_data[1]:,.2f}")
            print(f"Total Gaji: Rp{(gaji_data[0] + gaji_data[1]):,.2f}")

        # Input data baru (boleh kosong untuk tetap seperti lama)
        print("\nIsi dengan data baru (kosongkan jika tidak ingin diubah):")
        nama_baru = input(f"Nama [{pegawai[1]}]: ") or pegawai[1]
        umur_baru = input(f"Umur [{pegawai[2]}]: ") or pegawai[2]
        jk_baru = input(f"Jenis Kelamin [{pegawai[3]}] (L/P): ").upper() or pegawai[3]
        alamat_baru = input(f"Alamat [{pegawai[4]}]: ") or pegawai[4]

        if jk_baru not in ['L', 'P']:
            raise InvalidInputError("Jenis kelamin harus L atau P.")

        # Input gaji baru
        if gaji_data:
            gaji_pokok_baru = input(f"Gaji Pokok [{gaji_data[0]}]: ") or gaji_data[0]
            tunjangan_baru = input(f"Tunjangan [{gaji_data[1]}]: ") or gaji_data[1]
        else:
            gaji_pokok_baru = float(input("Gaji Pokok: "))
            tunjangan_baru = float(input("Tunjangan: "))

        gaji_pokok_baru = float(gaji_pokok_baru)
        tunjangan_baru = float(tunjangan_baru)
        total_gaji_baru = gaji_pokok_baru + tunjangan_baru

        # Update tabel pegawai
        sql_update_pegawai = """
            UPDATE pegawai SET
            nama = %s,
            umur = %s,
            jenis_kelamin = %s,
            alamat = %s
            WHERE id_pegawai = %s
        """
        val_pegawai = (nama_baru, int(umur_baru), jk_baru, alamat_baru, id_pegawai)
        cursor.execute(sql_update_pegawai, val_pegawai)

        # Update tabel gaji
        if gaji_data:
            sql_update_gaji = """
                UPDATE gaji SET
                gaji_pokok = %s,
                tunjangan = %s,
                total_gaji = %s
                WHERE id_pegawai = %s
            """
            val_gaji = (gaji_pokok_baru, tunjangan_baru, total_gaji_baru, id_pegawai)
            cursor.execute(sql_update_gaji, val_gaji)
        else:
            sql_insert_gaji = """
                INSERT INTO gaji (id_pegawai, gaji_pokok, tunjangan, total_gaji)
                VALUES (%s, %s, %s, %s)
            """
            val_gaji = (id_pegawai, gaji_pokok_baru, tunjangan_baru, total_gaji_baru)
            cursor.execute(sql_insert_gaji, val_gaji)

        db.commit()
        print("Data pegawai dan gaji berhasil diupdate.")

    except ValueError as ve:
        print(f"Input tidak valid: {ve}")
    except DataNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def tambah_absen(db, stack_absen):
    daftar_pekerja = load_daftar_pekerja(db)
    print("\nDAFTAR PEGAWAI:")
    for p in daftar_pekerja:
        p.tampilkan()
        print("-" * 30)

    try:
        id_pegawai = int(input("Pilih ID Pegawai untuk absen: "))
        pegawai_dipilih = next((p for p in daftar_pekerja if p.id_pegawai == id_pegawai), None)
        if not pegawai_dipilih:
            raise DataNotFoundError("Pegawai tidak ditemukan.")

        status = input("Status (Hadir/Izin/Sakit/Alpha): ").capitalize()
        if status not in ['Hadir', 'Izin', 'Sakit', 'Alpha']:
            raise InvalidInputError("Status harus Hadir/Izin/Sakit/Alpha.")

        absen_baru = {
            "id_pegawai": id_pegawai,
            "status": status
        }

        stack_absen.push(absen_baru)
        print(f"Absen untuk {pegawai_dipilih.nama} dimasukkan ke antrian.")
    except ValueError:
        print("Input harus berupa angka.")
    except DataNotFoundError as e:
        print(e)
    except InvalidInputError as e:
        print(e)

def undo_absen(stack_absen):
    try:
        absen_hapus = stack_absen.pop()
        print(f"Absen untuk ID {absen_hapus['id_pegawai']} dihapus dari antrian.")
    except EmptyStackException as e:
        print(e)

def lihat_queue_sekarang(stack_absen):
    antrian = stack_absen.lihat_stack()
    if antrian:
        print("\nANTRIAN SAAT INI:")
        for idx, a in enumerate(antrian, start=1):
            print(f"{idx}. ID Pegawai: {a['id_pegawai']}, Status: {a['status']}")
    else:
        print("Antrian kosong.")

def kirim_absen_ke_database(db, stack_absen):
    cursor = db.cursor()
    while not stack_absen.is_empty():
        absen = stack_absen.pop()
        sql = "INSERT INTO absensi (id_pegawai, tanggal, status_kehadiran) VALUES (%s, CURDATE(), %s)"
        val = (absen["id_pegawai"], absen["status"])
        cursor.execute(sql, val)
        db.commit()
        print(f"Absen untuk ID {absen['id_pegawai']} dikirim ke database.")
    print("Semua absen telah dikirim ke database.")

def tampilkan_semua_pegawai(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id_pegawai, p.nama, p.umur, p.jenis_kelamin, p.alamat,
               g.gaji_pokok, g.tunjangan, g.total_gaji
        FROM pegawai p
        LEFT JOIN gaji g ON p.id_pegawai = g.id_pegawai
    """)
    hasil = cursor.fetchall()
    
    if not hasil:
        print("Belum ada data pegawai.")
        return

    print("\nDAFTAR PEGAWAI:")
    for row in hasil:
        print("-" * 30)
        print(f"ID Pegawai   : {row[0]}")
        print(f"Nama         : {row[1]}")
        print(f"Umur         : {row[2]}")
        print(f"Jenis Kelamin: {row[3]}")
        print(f"Alamat       : {row[4]}")
        print(f"Gaji Pokok   : Rp{row[5]:,.2f}" if row[5] else "Gaji Pokok   : -")
        print(f"Tunjangan    : Rp{row[6]:,.2f}" if row[6] else "Tunjangan    : -")
        print(f"Total Gaji   : Rp{row[7]:,.2f}" if row[7] else "Total Gaji   : -")


def main():
    db = connect_db()
    stack_absen = StackAbsen()

    while True:
        tampilkan_menu()
        pilihan = input("Pilih opsi (1-8): ")

        if pilihan == '1':
            tambah_pegawai(db)
        elif pilihan == '2':
            hapus_pegawai(db)
        elif pilihan == '3':
            update_pegawai(db)
        elif pilihan == '4':
            tambah_absen(db, stack_absen)
        elif pilihan == '5':
            undo_absen(stack_absen)
        elif pilihan == '6':
            lihat_queue_sekarang(stack_absen)
        elif pilihan == '7':
            kirim_absen_ke_database(db, stack_absen)
        elif pilihan == '8':
            tampilkan_semua_pegawai(db)
        elif pilihan == '9':
            print("Keluar dari sistem...")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()