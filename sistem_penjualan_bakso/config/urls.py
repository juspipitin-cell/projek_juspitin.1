"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # ✅ Panel admin Django default
    path('admin-django/', admin.site.urls),

    # ✅ Home dan Autentikasi
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # =========================== 👤 ADMIN pitin1 ===========================
    path('admin/produk/tambah/', views.admin_tambah_produk, name='admin_tambah_produk'),
    path('admin/produk/tampil/', views.admin_tampil_produk, name='admin_tampil_produk'),
    path('admin/produk/edit/<int:id>/', views.admin_edit_produk, name='admin_edit_produk'),
    path('admin/produk/hapus/<int:id>/', views.admin_hapus_produk, name='admin_hapus_produk'),
    path('admin/laporan/', views.admin_laporan_penjualan, name='admin_laporan_penjualan'),

    # =========================== 👥 KASIR selain pitin1 ===========================
    path('kasir/penjualan/tambah/', views.kasir_tambah_penjualan, name='kasir_tambah_penjualan'),
    path('kasir/penjualan/tampil/', views.kasir_tampil_penjualan, name='kasir_tampil_penjualan'),
    path('kasir/transaksi/<int:id>/cetak/', views.kasir_cetak_transaksi, name='kasir_cetak_transaksi'),

]
