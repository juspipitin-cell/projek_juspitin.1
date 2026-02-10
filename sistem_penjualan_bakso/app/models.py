from django.db import models
from django.contrib.auth.models import User


class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.PositiveIntegerField()
    stok = models.PositiveIntegerField()

    def __str__(self):
        return self.nama


class Transaksi(models.Model):
    pelanggan = models.CharField(max_length=100)
    kasir = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal = models.DateTimeField(auto_now_add=True)

    @property
    def total_transaksi(self):
        return sum(item.total_harga for item in self.penjualan_set.all())

    def __str__(self):
        return f"Transaksi {self.id} - {self.pelanggan} ({self.tanggal.strftime('%d-%m-%Y')})"


class Penjualan(models.Model):
    transaksi = models.ForeignKey(
        Transaksi,
        on_delete=models.CASCADE,
        null=True,   # Optional saat membuat manual
        blank=True
    )
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    total_harga = models.PositiveIntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produk.nama} x {self.jumlah} (Rp {self.total_harga:,})"
