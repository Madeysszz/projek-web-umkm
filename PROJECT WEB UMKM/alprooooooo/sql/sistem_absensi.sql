CREATE DATABASE sistem_absensi;
USE sistem_absensi;

-- 1. Pegawai
CREATE TABLE pegawai (
    id_pegawai INT PRIMARY KEY,
    nama VARCHAR(100),
    umur INT,
    jenis_kelamin ENUM('L', 'P'),
    alamat TEXT
);

-- 2. Jabatan
CREATE TABLE jabatan (
    id_jabatan INT PRIMARY KEY,
    nama_jabatan VARCHAR(50)
);

-- 3. Departemen
CREATE TABLE departemen (
    id_departemen INT PRIMARY KEY,
    nama_departemen VARCHAR(50)
);

-- 4. Gaji
CREATE TABLE gaji (
    id_gaji INT AUTO_INCREMENT PRIMARY KEY,
    id_pegawai INT,
    gaji_pokok DECIMAL(10,2),
    tunjangan DECIMAL(10,2),
    total_gaji DECIMAL(10,2),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- 5. Absensi
CREATE TABLE absensi (
    id_absen INT AUTO_INCREMENT PRIMARY KEY,
    id_pegawai INT,
    tanggal DATE,
    status_kehadiran ENUM('Hadir', 'Izin', 'Sakit', 'Alpha'),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- Jabatan
INSERT INTO jabatan VALUES
(1, 'Staff'), (2, 'Supervisor'), (3, 'Manager'), (4, 'Asisten Manager'), (5, 'Direktur'),
(6, 'Admin'), (7, 'HRD'), (8, 'IT Support'), (9, 'Akuntan'), (10, 'Marketing');

-- Departemen
INSERT INTO departemen VALUES
(1, 'IT'), (2, 'Keuangan'), (3, 'SDM'), (4, 'Operasional'), (5, 'Marketing'),
(6, 'Produksi'), (7, 'R&D'), (8, 'Customer Service'), (9, 'Logistik'), (10, 'Legal');

-- Pegawai
INSERT INTO pegawai VALUES
(1, 'Ahmad', 28, 'L', 'Jakarta'),
(2, 'Maisaroh', 25, 'P', 'Bandung'),
(3, 'Rizal', 30, 'L', 'Surabaya'),
(4, 'Budi', 27, 'L', 'Semarang'),
(5, 'Siti', 26, 'P', 'Medan'),
(6, 'Adi', 32, 'L', 'Yogyakarta'),
(7, 'Indah', 29, 'P', 'Palembang'),
(8, 'Fajar', 24, 'L', 'Makassar'),
(9, 'Nina', 25, 'P', 'Denpasar'),
(10, 'Agus', 35, 'L', 'Padang');

-- Gaji
INSERT INTO gaji (id_pegawai, gaji_pokok, tunjangan, total_gaji) VALUES
(1, 8000000, 2000000, 10000000),
(2, 6000000, 1500000, 7500000),
(3, 5000000, 1000000, 6000000),
(4, 7000000, 1800000, 8800000),
(5, 7500000, 2000000, 9500000),
(6, 5500000, 1200000, 6700000),
(7, 6500000, 1500000, 8000000),
(8, 5800000, 1300000, 7100000),
(9, 6200000, 1400000, 7600000),
(10, 7200000, 1700000, 8900000);

-- Absensi (opsional)
INSERT INTO absensi (id_pegawai, tanggal, status_kehadiran) VALUES
(1, CURDATE(), 'Hadir'),
(2, CURDATE(), 'Hadir'),
(3, CURDATE(), 'Sakit'),
(4, CURDATE(), 'Hadir'),
(5, CURDATE(), 'Izin'),
(6, CURDATE(), 'Hadir'),
(7, CURDATE(), 'Alpha'),
(8, CURDATE(), 'Hadir'),
(9, CURDATE(), 'Hadir'),
(10, CURDATE(), 'Hadir');