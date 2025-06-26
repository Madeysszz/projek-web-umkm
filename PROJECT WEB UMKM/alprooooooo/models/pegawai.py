# models/pegawai.py

class Pegawai:
    def __init__(self, id_pegawai, nama, umur, jenis_kelamin, alamat):
        self.id_pegawai = id_pegawai
        self.nama = nama
        self.umur = umur
        self.jenis_kelamin = jenis_kelamin
        self.alamat = alamat

    def tampilkan(self):
        print(f"ID Pegawai: {self.id_pegawai}")
        print(f"Nama: {self.nama}")
        print(f"Umur: {self.umur}")
        print(f"Jenis Kelamin: {self.jenis_kelamin}")
        print(f"Alamat: {self.alamat}")