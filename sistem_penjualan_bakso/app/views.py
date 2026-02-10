from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Produk, Penjualan, Transaksi
from django.utils import timezone

# ========= BERANDA =========
def home(request):
    return render(request, 'home.html')

# ========= LOGIN & LOGOUT =========
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# ========================== 👤 ADMIN AREA (pitin1) ==========================

@login_required
def admin_tambah_produk(request):
    if request.user.username != 'pitin1':
        return redirect('home')

    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        harga = request.POST.get('harga', '').strip()
        stok = request.POST.get('stok', '').strip()

        if not nama or not harga or not stok:
            return render(request, 'pitin1/produk_tambah.html', {
                'error': 'Semua field wajib diisi.',
                'nama': nama,
                'harga': harga,
                'stok': stok,
            })

        try:
            harga = int(harga)
            stok = int(stok)
        except ValueError:
            return render(request, 'pitin1/produk_tambah.html', {
                'error': 'Harga dan stok harus berupa angka.',
                'nama': nama,
                'harga': harga,
                'stok': stok,
            })

        # 🔍 Cek apakah produk dengan nama tersebut sudah ada
        existing = Produk.objects.filter(nama__iexact=nama).first()

        if existing:
            # ✅ Perbarui stok dan harga
            existing.stok += stok
            existing.harga = harga  # Optional: hanya jika ingin perbarui harga juga
            existing.save()
        else:
            # ➕ Tambahkan produk baru
            Produk.objects.create(nama=nama, harga=harga, stok=stok)

        return redirect('admin_tampil_produk')

    return render(request, 'pitin1/produk_tambah.html')


@login_required
def admin_tampil_produk(request):
    if request.user.username != 'pitin1':
        return redirect('home')
    data = Produk.objects.all()
    return render(request, 'pitin1/produk_tampil.html', {'data': data})

@login_required
def admin_edit_produk(request, id):
    if request.user.username != 'pitin1':
        return redirect('home')
    
    produk = get_object_or_404(Produk, id=id)

    if request.method == 'POST':
        produk.nama = request.POST.get('nama')
        produk.harga = int(request.POST.get('harga'))
        stok_tambah = int(request.POST.get('stok_tambah', 0))
        produk.stok += stok_tambah
        produk.save()
        return redirect('admin_tampil_produk')

    return render(request, 'pitin1/produk_edit.html', {'produk': produk})

@login_required
def admin_hapus_produk(request, id):
    if request.user.username != 'pitin1':
        return redirect('home')
    produk = get_object_or_404(Produk, id=id)
    produk.delete()
    return redirect('admin_tampil_produk')

@login_required
def admin_laporan_penjualan(request):
    if request.user.username != 'pitin1':
        return redirect('home')

    data = Penjualan.objects.select_related('produk', 'transaksi').all().order_by('-tanggal')
    
    total_semua = sum(item.total_harga for item in data)

    return render(request, 'pitin1/laporan_penjualan.html', {
        'data': data,
        'total_semua': total_semua
    })



# ========================== 👨‍💼 KASIR AREA (selain pitin1) ==========================

@login_required
def kasir_tambah_penjualan(request):
    if request.user.username == 'pitin1':
        return redirect('home')

    produk_list = Produk.objects.all()

    if request.method == 'POST':
        pelanggan = request.POST.get('pelanggan')
        produk_ids = request.POST.getlist('produk')
        jumlahs = request.POST.getlist('jumlah')

        if not pelanggan or not produk_ids:
            return render(request, 'penjualan/tambah.html', {'produk': produk_list, 'error': 'Lengkapi semua data.'})

        transaksi = Transaksi.objects.create(
            pelanggan=pelanggan,
            kasir=request.user,
            tanggal=timezone.now()
        )

        for produk_id, jumlah in zip(produk_ids, jumlahs):
            if not jumlah:
                continue  # lewati jika kosong
            produk = Produk.objects.get(id=produk_id)
            jumlah = int(jumlah)

            if produk.stok >= jumlah:
                produk.stok -= jumlah
                produk.save()

                Penjualan.objects.create(
                    transaksi=transaksi,
                    produk=produk,
                    jumlah=jumlah,
                    total_harga=produk.harga * jumlah,
                    tanggal=timezone.now()
                )

        return redirect('kasir_tampil_penjualan')

    return render(request, 'penjualan/tambah.html', {'produk': produk_list})


@login_required
def kasir_tampil_penjualan(request):
    if request.user.username == 'pitin1':
        return redirect('home')

    transaksi_list = Transaksi.objects.filter(kasir=request.user).order_by('-tanggal').prefetch_related('penjualan_set', 'penjualan_set__produk')
    return render(request, 'penjualan/tampil.html', {'transaksi_list': transaksi_list})

@login_required
def kasir_cetak_transaksi(request, id):
    if request.user.username == 'pitin1':
        return redirect('home')

    transaksi = get_object_or_404(Transaksi, id=id, kasir=request.user)
    penjualan_list = transaksi.penjualan_set.select_related('produk').all()
    total_harga = sum(item.total_harga for item in penjualan_list)

    return render(request, 'penjualan/cetak_transaksi.html', {
        'transaksi': transaksi,
        'penjualan_list': penjualan_list,
        'total_harga': total_harga
    })

