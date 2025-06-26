# models/absensi.py
from datetime import date

class Absensi:
    def __init__(self, id_absen, id_pegawai, tanggal=None, status='Hadir'):
        self.id_absen = id_absen
        self.id_pegawai = id_pegawai
        self.tanggal = tanggal or date.today()
        self.status = status

    def tampilkan(self):
        print(f"ID Absen: {self.id_absen}")
        print(f"ID Pegawai: {self.id_pegawai}")
        print(f"Tanggal: {self.tanggal}")
        print(f"Status: {self.status}")