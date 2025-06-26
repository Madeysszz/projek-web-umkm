# models/gaji.py

class Gaji:
    def __init__(self, id_gaji, id_pegawai, gaji_pokok, tunjangan, total_gaji):
        self.id_gaji = id_gaji
        self.id_pegawai = id_pegawai
        self.gaji_pokok = gaji_pokok
        self.tunjangan = tunjangan
        self.total_gaji = total_gaji