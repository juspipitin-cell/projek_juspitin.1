from django.urls import path
from . import views

urlpatterns = [
    # ... URL lain
    path('produk/edit/<int:id>/', views.edit_produk, name='edit_produk'),
    path('produk/hapus/<int:id>/', views.hapus_produk, name='hapus_produk'),
    path('kasir/transaksi/<int:id>/cetak/', views.kasir_cetak_transaksi, name='kasir_cetak_transaksi'),

]
