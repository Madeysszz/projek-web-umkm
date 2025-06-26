<?php
session_start();
if (!isset($_SESSION["admin_id"])) {
    header("Location: login.php");
    exit();
}

// Include database connection
include('../config/db.php'); // Pastikan path ini benar

// Query untuk mengambil jumlah total pesanan
$queryTotalPesanan = "SELECT COUNT(*) AS total_pesanan FROM pesanan";
$resultTotalPesanan = $conn->query($queryTotalPesanan);
$totalPesanan = $resultTotalPesanan->fetch_assoc()['total_pesanan'];

// Query untuk total pendapatan (hanya untuk pesanan yang selesai)
$queryTotalPendapatan = "SELECT SUM(total_harga) AS total_pendapatan FROM pesanan WHERE status = 'Selesai'";
$resultTotalPendapatan = $conn->query($queryTotalPendapatan);
$totalPendapatan = $resultTotalPendapatan->fetch_assoc()['total_pendapatan'];

// Query untuk jumlah pesanan yang selesai
$queryPesananSelesai = "SELECT COUNT(*) AS pesanan_selesai FROM pesanan WHERE status = 'Selesai'";
$resultPesananSelesai = $conn->query($queryPesananSelesai);
$pesananSelesai = $resultPesananSelesai->fetch_assoc()['pesanan_selesai'];

// Query untuk jumlah pelanggan terdaftar
$queryTotalPelanggan = "SELECT COUNT(*) AS total_pelanggan FROM pelanggan";
$resultTotalPelanggan = $conn->query($queryTotalPelanggan);
$totalPelanggan = $resultTotalPelanggan->fetch_assoc()['total_pelanggan'];

// Query untuk menghitung pendapatan sebulan
$queryRataRataPendapatan = "SELECT AVG(total_harga) AS rata_rata_pendapatan FROM pesanan WHERE status = 'Selesai'";
$resultRataRataPendapatan = $conn->query($queryRataRataPendapatan);
$rataRataPendapatan = $resultRataRataPendapatan->fetch_assoc()['rata_rata_pendapatan'];

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Admin UMKM</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">

    <div class="flex">
        <!-- Sidebar -->
        <div class="w-64 bg-pink-900 text-white h-screen p-5">
            <h2 class="text-2xl font-bold mb-5">Admin Dashboard</h2>
            <ul>
                <li><a href="produk/index.php" class="block py-2 px-4 rounded hover:bg-pink-700">Manajemen Produk</a></li>
                <li><a href="kategori/index.php" class="block py-2 px-4 rounded hover:bg-pink-700">Manajemen Kategori</a></li>
                <li><a href="pelanggan/index.php" class="block py-2 px-4 rounded hover:bg-pink-700">Manajemen Pelanggan</a></li>
                <li><a href="pesanan/index.php" class="block py-2 px-4 rounded hover:bg-pink-700">Manajemen Pesanan</a></li>
                <li><a href="pembayaran/index.php" class="block py-2 px-4 rounded hover:bg-pink-700">Manajemen Pembayaran</a></li>
                <li><a href="pengiriman/index.php" class="block py-2 px-4 rounded hover:bg-pink-700">Manajemen Pengiriman</a></li>
                <li><a href="logout.php" class="block py-2 px-4 rounded hover:bg-pink-700">Logout</a></li>
            </ul>
        </div>

        <!-- Main content -->
        <div class="flex-1 p-10">
            <h1 class="text-3xl font-bold text-gray-800 mb-5">Selamat datang, <?= $_SESSION["admin_name"] ?></h1>
            
            <!-- Statistik -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="bg-white p-5 rounded shadow-md">
                    <h3 class="text-xl font-semibold text-gray-700">Total Pesanan</h3>
                    <p class="text-2xl text-gray-900"><?= $totalPesanan ?></p>
                </div>

                <div class="bg-white p-5 rounded shadow-md">
                    <h3 class="text-xl font-semibold text-gray-700">Total Pendapatan</h3>
                    <p class="text-2xl text-gray-900">Rp <?= number_format($totalPendapatan, 2, ',', '.') ?></p>
                </div>

                <div class="bg-white p-5 rounded shadow-md">
                    <h3 class="text-xl font-semibold text-gray-700">Rata-rata Hasil Sebulan</h3>
                    <p class="text-2xl text-gray-900">Rp <?= number_format($rataRataPendapatan, 2, ',', '.') ?></p>
                </div>

                <div class="bg-white p-5 rounded shadow-md">
                    <h3 class="text-xl font-semibold text-gray-700">Pesanan Selesai</h3>
                    <p class="text-2xl text-gray-900"><?= $pesananSelesai ?></p>
                </div>

                <div class="bg-white p-5 rounded shadow-md">
                    <h3 class="text-xl font-semibold text-gray-700">Total Pelanggan</h3>
                    <p class="text-2xl text-gray-900"><?= $totalPelanggan ?></p>
                </div>
            </div>

            <div class="mt-5">
                <p class="text-lg">Pilih menu di sebelah kiri untuk mengelola produk atau kategori.</p>
            </div>
        </div>
    </div>

</body>
</html>
