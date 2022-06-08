from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import date
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from imp import C_BUILTIN
from django.db.models import Sum, Count
import pandas as pd

def logout(request):
    return render(request,'gara/logout.html',{})

def home(request):
    return render(request, 'gara/home.html',{})

def is_staff(user):
    return user.groups.filter(name='STAFF').exists()

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

@user_passes_test(is_admin)
@login_required(login_url='/login')
def createStaffAccount(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data)
            print('valid')
            username = request.POST['username']
            password = request.POST['password']
            lastname = request.POST['lastname']
            firstname = request.POST['firstname']
            mobile = request.POST['mobile']
            emails = request.POST['emails']
            profile_pic = request.FILES['profile_pic']
            address = request.POST['address']
            Staff.objects.create(username=username, password=password, lastname=lastname,
                                    firstname=firstname, mobile=mobile, emails=emails, 
                                    address=address , profile_pic=profile_pic)
            user = User.objects.create_user(username=username, password=password, 
                                first_name=firstname, last_name=lastname, email=emails)
            user.is_staff = True
            user.save()
            my_customer_group = Group.objects.get_or_create(name='STAFF')
            my_customer_group[0].user_set.add(user)
            messages.success(request, f'Add staff {username} successfully! !!')
        else:
            messages.warning(request,'Invalid form, please filling a again!')
    context = {'userForm': form, 'username':request.user.username}
    return render(request, 'profile/create_new_staff.html', context)

def customer_login_view(request):
    form = AuthenticationForm()
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['rawpassword'] = password
        print(f'username {username} password {password}')
        print(form.is_valid())
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('Log In sucessfully')
            return redirect(f'../profile/{username}')
        else:
            messages.warning(request, 'Đăng nhập thất bại! Kiểm tra thông tin của bạn và đăng nhập lại')
    context = {'form': form}
    
    return render(request, 'profile/customerlogin.html', context)

@login_required(login_url='/login')
def profile(request, username):
    try:
        cus = Staff.objects.get(username=username)
        profile_pic = '../' + cus.profile_pic.url
        print(profile_pic)
    except:
        rawpassword = request.session.get('rawpassword')
        password = request.user.password
        cus = Staff.objects.create(username=username, password=rawpassword)
        cus.is_admin = True
        profile_pic = "../static/profile_pic/CustomerProfilePic/images.jpg"
        cus.profile_pic = profile_pic
        user = User.objects.get(username=username, password=password)
        user.save()
        my_customer_group = Group.objects.get_or_create(name='ADMIN')
        my_customer_group[0].user_set.add(user)
        cus.save()

    context = {'customer': cus, 'username': username, 'picture': profile_pic}
    return render(request,'profile/Profile.html', context)



@login_required(login_url='/login')
def customer_dashboard_view(request, username):
    cus = Staff.objects.get(username=username)
    profile_pic = '../' + cus.profile_pic.url
    context = {'customer': cus, 'username': username, 'picture': profile_pic}
    return render(request, 'profile/customer_dashboard.html', context)

@login_required(login_url='/login')
def edit_customer_profile_view(request, username):
    staff = get_object_or_404(Staff, username=username)
    staffUpdate_form = StaffUpdateForm(instance= staff)
    picture = '../' + staff.profile_pic.url
    print(staff)
    if request.method=='POST':
        staffUpdate_form = StaffUpdateForm(request.POST, request.FILES, instance=staff)
        if staffUpdate_form.is_valid():
            print('valid')
            staff = staffUpdate_form.save()
            staff.save()
            return HttpResponseRedirect(f'../profile/{username}')
    mydict={'customerForm':staffUpdate_form, 'picture': picture}
    return render(request,'profile/edit_customer_profile.html',mydict)

@login_required(login_url='/login')
def edit_customer_account_view(request, username):
    staff = get_object_or_404(Staff, username=username)
    user = User.objects.get(username=request.user.username)
    StaffUpdate_Account = StaffUpdateAccount(instance=staff)
    picture = '../' + staff.profile_pic.url
    if request.method=='POST':
        StaffUpdate_Account = StaffUpdateAccount(request.POST ,instance=staff)
        print(StaffUpdate_Account.errors)
        if StaffUpdate_Account.is_valid():
            print('valid')
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.save()
            staff = StaffUpdate_Account.save()
            staff.password = request.POST['password']
            staff.save()
            return redirect('../login')
    mydict = {'userForm':StaffUpdate_Account, 'picture':picture}
    return render(request,'profile/edit_customer_account.html', mydict)

#------------------------------------------------------------------------------
@login_required(login_url='/login')
def nhapbienso_phieuthu(request, username):
    enquiry= NhapBienSoThu()
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if request.method=='POST':
        enquiry= NhapBienSoThu(request.POST)
        if enquiry.is_valid():
            print('enquiry is valid')
            print(request.POST['bienso'])
            xe_x=Xe.objects.get(maxe=request.POST['bienso']) 
            return redirect(f'../{username}/nhap_phieuthu/{xe_x.maxe}')
    context= {'enquiry':enquiry, 'customer': staff, 'picture': picture}        
    return render(request,'phieuthutien/nhapbienso_phieuthu.html',context)

@login_required(login_url='/login')
def xacnhan_phieuthu(request,maxe, username):
    nhapsotienthu=NhapSoTienThu()
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    xe_x=Xe.objects.get(maxe=maxe)
    khach_x=KhachHang.objects.get(makhachhang=xe_x.makhachhang_id) 
    list_phieusua=PhieuSuaChua.objects.all().filter(maxe_id=xe_x.maxe)
    xe_x.save()
    context= {'nhapsotienthu':nhapsotienthu,'xe_x': xe_x,'khach_x':khach_x, 
                "customer": staff, "picture":picture, "data":list_phieusua} 
    if request.method=='POST':
        nhapsotienthu=NhapSoTienThu(request.POST)  
        if nhapsotienthu.is_valid():
            print('enquiry is valid')
            tienthu=nhapsotienthu.cleaned_data['sotienthu']
            if tienthu>xe_x.tienno:
                messages.warning(request, 'Số tiền nhập không hợp lệ')
                return render(request,'phieuthutien/nhapsotienthu.html',context)  
            elif tienthu<=xe_x.tienno: 
                phieuthutien_x=PhieuThuTien.objects.create(maxe_id=xe_x.maxe,sotienthu=tienthu)
                xe_x.tienno-= tienthu
                xe_x.save()
                print('da luu vao database')
                messages.success(request, 'Thanh toán thành công!')

    return render(request,'phieuthutien/nhapsotienthu.html',context)       

@login_required(login_url="/login")
def view_phieuthu(request,maphieuthutien):
    phieuthu=PhieuThuTien.objects.get(maphieuthutien=maphieuthutien)
    xe_x=Xe.objects.get(maxe=phieuthu.maxe)
    context={'xe_x':xe_x,'phieuthu':phieuthu}
    return render(request,'phieuthutien/view_phieuthu.html',context)       

@login_required(login_url="/login")
def nhapbiensosua(request,username):
    enquiry= NhapBienSoSua()
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if request.method=='POST':
        enquiry=NhapBienSoSua(request.POST)
        print(request.POST['bienso'])
        xe_x=Xe.objects.get(bienso=request.POST['bienso'])
        phieusua_x=PhieuSuaChua.objects.create(maxe_id=xe_x.maxe,tongthanhtien=0)
        phieusua_x.save()
        return redirect(f'../{username}/view_phieusua/{phieusua_x.maphieusuachua}')
    return render(request,'phieusuachua/nhapbiensosua.html', {'enquiry':enquiry, 'customer': staff, 'picture':picture}, ) 

@login_required(login_url="/login")
def view_phieusua(request ,maphieusuachua, username):
    phieusua=PhieuSuaChua.objects.get(maphieusuachua=maphieusuachua)
    xe_x=Xe.objects.get(maxe=phieusua.maxe_id)
    data=CT_PhieuSuaChua.objects.all().filter(maphieusuachua=maphieusuachua)
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    enquiry=NhapCTSuaChua()
    context= {'phieusua':phieusua,'xe_x':xe_x,'data':data,'enquiry':enquiry, "customer":staff, "picture":picture}
    if request.method=='POST':
        print('request method la POST')
        enquiry=NhapCTSuaChua(request.POST)
        if enquiry.is_valid():
            print('enquiry is valid')
            tiencong_x=TienCong.objects.get(loaitiencong=enquiry.cleaned_data['loaitiencong'])
            tongtiencong=tiencong_x.tiencong*enquiry.cleaned_data['solan']
            phieusua_x=CT_PhieuSuaChua.objects.create(maphieusuachua_id=maphieusuachua,
            matiencong_id=tiencong_x.matiencong,tiencong=tongtiencong,
            solan=enquiry.cleaned_data['solan'], noidung=enquiry.cleaned_data['noidung'],tongtien=tongtiencong)
            tongthanhtien_x=phieusua.tongthanhtien+tongtiencong
            phieusua.tongthanhtien=tongthanhtien_x
            phieusua.save()
            #Cap nhat tien no
            xe_x=Xe.objects.get(maxe=phieusua.maxe_id)
            tienno_xe=xe_x.tienno+tongtiencong
            xe_x.tienno=tienno_xe
            xe_x.save()
            return render(request,'phieusuachua/view_phieusua.html',context) 
    return render(request,'phieusuachua/view_phieusua.html',context) 


@login_required(login_url="/login")
def view_ctphieusuachua(request,mact_phieusuachua, username):
    ct_phieusua=CT_PhieuSuaChua.objects.get(mact_phieusuachua=mact_phieusuachua)  
    data=CT_VatTuPhuTung.objects.all().filter(mact_phieusuachua=mact_phieusuachua)
    nhap_ctvtpt=NhapCT_VatTuPhuTung
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    # context={'nhap_ctvtpt':nhap_ctvtpt}
    if request.method=='POST':
        print('request method is POST')
        nhap_ctvtpt=NhapCT_VatTuPhuTung(request.POST)
        if nhap_ctvtpt.is_valid():  
            print('phieu nhap is valid')
            vattu_x=VatTuPhuTung.objects.get(tenvattuphutung=nhap_ctvtpt.cleaned_data['tenvattuphutung'])
            hieuso=nhap_ctvtpt.cleaned_data['soluong']-vattu_x.soluong   #Dùng để so sánh số lượng nhập với số lượng trong kho
            if hieuso>0:
                messages.warning(request, 'Số lượng vật tư trong kho không đủ')
            else:
                #Tự động nhân đơn giá vật tư
                print('soluong du')
                dongia_ban= vattu_x.dongia*(QuyDinhHienHanh.objects.get(TenThamSo='Ti le don gia vtpt').GiaTri/100)
                #end
                tien1_ctvattu=dongia_ban*nhap_ctvtpt.cleaned_data['soluong']
                CT_VatTuPhuTung.objects.create(mact_phieusuachua_id=mact_phieusuachua,
                mavattuphutung_id=vattu_x.mavattuphutung, soluong=nhap_ctvtpt.cleaned_data['soluong'],
                dongia=dongia_ban, tongthanhtien=tien1_ctvattu)
                tong_tatcavattu=tien1_ctvattu+ct_phieusua.tongtienvattu
                ct_phieusua.tongtienvattu=tong_tatcavattu
                ct_phieusua.tongtien=tong_tatcavattu+ct_phieusua.tiencong
                ct_phieusua.save()
                phieusua_x=PhieuSuaChua.objects.get(maphieusuachua=ct_phieusua.maphieusuachua_id)
                tong_phieusua=phieusua_x.tongthanhtien + tien1_ctvattu
                phieusua_x.tongthanhtien=tong_phieusua
                phieusua_x.save()
                            #cap nhat tien no xe
                xe_x=Xe.objects.get(maxe=phieusua_x.maxe_id)
                tienno_xe=xe_x.tienno+tien1_ctvattu
                xe_x.tienno=tienno_xe
                xe_x.save()
                #cap nhat so luong vat tu
                vattu_x.soluong= -1* hieuso
                vattu_x.save()
                # capnhattienno(phieusua_x.maphieusuachua,tong_phieusua)
    
            # capnhattienno(phieusua_x.maphieusuachua,tong_phieusua)                         
    context={'ct_phieusua':ct_phieusua,'nhap_ctvtpt':nhap_ctvtpt,'data':data,"customer":staff, "picture":picture}
    return render(request,'phieusuachua/view_ctphieusua.html',context)

@login_required(login_url="/login")
def delete_ctphieusua(request,mact_phieusuachua,username):
    ctphieusua=CT_PhieuSuaChua.objects.get(mact_phieusuachua=mact_phieusuachua)
    phieusua_x=PhieuSuaChua.objects.get(maphieusuachua=ctphieusua.maphieusuachua_id)
    print(phieusua_x.tongthanhtien,'-',ctphieusua.tongtien)
    tongthanhtien_x=phieusua_x.tongthanhtien-ctphieusua.tongtien
    phieusua_x.tongthanhtien=tongthanhtien_x
    print(phieusua_x.tongthanhtien)
    #cap nhat tien no xe
    xe_x=Xe.objects.get(maxe=phieusua_x.maxe_id)
    tienno_xe=xe_x.tienno-ctphieusua.tongtien
    xe_x.tienno=tienno_xe
    xe_x.save()
    phieusua_x.save()
    ctphieusua.delete()
    maphieusuachua_x=int(phieusua_x.maphieusuachua)
    return redirect(f'../../{username}/view_phieusua/{phieusua_x.maphieusuachua}')

@login_required(login_url="/login")
def delete_chitietvattu(request,mact_vattuphutung,mact_phieusuachua,maphieusuachua,username):
    ctvt=CT_VatTuPhuTung.objects.get(mact_vattuphutung=mact_vattuphutung)
    ctphieusua=CT_PhieuSuaChua.objects.get(mact_phieusuachua=mact_phieusuachua)
    phieusua_x=PhieuSuaChua.objects.get(maphieusuachua=maphieusuachua)
    tien_1vattu=ctvt.soluong*ctvt.dongia
    tongtien=ctphieusua.tongtien-tien_1vattu
    tongtienvattu_x=ctphieusua.tongtienvattu-tien_1vattu
    ctphieusua.tongtienvattu=tongtienvattu_x
    ctphieusua.tongtien=tongtien
    tongthanhtien_x=phieusua_x.tongthanhtien-tien_1vattu
    phieusua_x.tongthanhtien=tongthanhtien_x
    #cap nhat tien no xe
    xe_x=Xe.objects.get(maxe=phieusua_x.maxe_id)
    tienno_xe=xe_x.tienno-tien_1vattu
    xe_x.tienno=tienno_xe
    xe_x.save()
    #cap nhat lai so luong
    vattu_x=VatTuPhuTung.objects.get(mavattuphutung=ctvt.mavattuphutung_id)
    soluongcapnhat=vattu_x.soluong+ctvt.soluong
    vattu_x.soluong=soluongcapnhat
    vattu_x.save()
    ctphieusua.save()
    phieusua_x.save()
    ctvt.delete()
    return redirect(f'/../../{username}/view_ctphieusua/{ctphieusua.mact_phieusuachua}')

#------------------------------------------------------------------------------------------------------------------------

@login_required(login_url="/login")
def tiep_nhan(request, username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    enquiry=TiepNhanForm()
    count = PhieuTiepNhan.objects.filter(date=date.today()).count()
    if count > QuyDinhHienHanh.objects.get(TenThamSo='So xe sua chua toi da').GiaTri:
        enquiries=PhieuTiepNhan.objects.all().filter(date=date.today())
        messages.warning(request, 'Đã quá hạn số lượng tiếp nhận trong ngày')
        return HttpResponseRedirect('request')

    if request.method=='POST':
        enquiry=TiepNhanForm(request.POST)
        if enquiry.is_valid():
            enquiry_x=enquiry.save()
            try:
                kh = KhachHang.objects.all().filter(tenkhachhang=enquiry_x.tenchuxe, dienthoai=enquiry_x.dienthoai)[0]
            except:
                kh = False
            if not kh:
                kh = KhachHang(tenkhachhang=enquiry_x.tenchuxe, dienthoai=enquiry_x.dienthoai, diachi=enquiry_x.diachi)
                kh.save()
            xe = Xe.objects.all().filter(bienso=enquiry_x.bienso, makhachhang=kh, mahieuxe=enquiry_x.hieuxe)
            if not xe:
                xe = Xe(bienso=enquiry_x.bienso, makhachhang=kh, mahieuxe=enquiry_x.hieuxe)
                xe.save()

        return HttpResponseRedirect('request')
    
    return render(request,'gara/add_request.html',{'enquiry':enquiry, 'customer': staff, "picture": picture})

@login_required(login_url="/login")
def view_request(request, username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    enquiry=PhieuTiepNhan.objects.all().filter(date=date.today())
    return render(request,'gara/view_request.html', {'enquiries': enquiry, 'customer': staff, "picture": picture})

@login_required(login_url="/login")
def view_baocaoton(request, username):
    form=AskDateForm()
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if request.method == 'POST':
        month = request.POST['month']
        BCT = None
        try:
            BCT = BaoCaoTon.objects.filter(date__year=month.split('-')[0], date__month=month.split('-')[1])
        except:
            return render(request,'gara/date_to_report.html',{'form':form, 'customer': staff, "picture": picture})
        if BCT: 
            enquiry = ct_baocaoton.objects.all().filter(MaBCT=BCT[len(BCT)-1].MaBCT).order_by('-MaVTPT_id').reverse()
            return render(request, 'gara/baocaoton.html',  {'enquiries': enquiry, 'month': month, 'customer':staff, "picture": picture})
        else:
            return render(request,'gara/date_to_report.html',{'form':form, 'customer': staff, "picture": picture})

    return render(request,'gara/date_to_report.html',{'form':form, 'customer':staff, "picture": picture})
@login_required(login_url="/login")
def update_request(request , username, pk):
    
    staff = Staff.objects.get(username=username)
    
    picture = '../' + staff.profile_pic.url
    ptn = PhieuTiepNhan.objects.get(maphieutiepnhan=pk)
    enquiry=TiepNhanForm()

    if request.method=='POST':
        enquiry=TiepNhanForm(request.POST)
        if enquiry.is_valid():
            enquiry_x=enquiry.save()
            try:
                kh = KhachHang.objects.all().filter(tenkhachhang=enquiry_x.tenchuxe, dienthoai=enquiry_x.dienthoai)[0]
            except:
                kh = False
            if not kh:
                kh = KhachHang(tenkhachhang=enquiry_x.tenchuxe, dienthoai=enquiry_x.dienthoai, diachi=enquiry_x.diachi)
                kh.save()
            xe = Xe.objects.all().filter(bienso=enquiry_x.bienso, makhachhang=kh, mahieuxe=enquiry_x.hieuxe)
            if not xe:
                xe = Xe(bienso=enquiry_x.bienso, makhachhang=kh, mahieuxe=enquiry_x.hieuxe)
                xe.save()

        return HttpResponseRedirect('request')
    return render(request,'gara/update_request.html',{'ptn':ptn,'enquiry':enquiry, 'customer': staff, "picture": picture})

@login_required(login_url="/login")
def save_baocaoton(request, username):
    now = date.today()
    bct_before = BaoCaoTon.objects.filter(date__year=now.year, 
                    date__month=now.month-1)
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    BCT = BaoCaoTon(date=date)
    BCT.save()
    vtpt = VatTuPhuTung.objects.all()
    
    if bct_before:
        
        for item in vtpt:
            toncuoi = item.soluong
            
            try:
                phatsinh = PhieuNhapVTPT.objects.get(date__year=now.year, date__month=now.month,mavattuphutung=item).soluong

            except:
                phatsinh = 0
            try:
                tondau = bct_before.objects.all().filter(MaVTPT=item.mavattuphutung)[0].TonCuoi
            except:
                tondau=0
            tempt = ct_baocaoton(MaBCT=BCT, MaVTPT=item, TonDau=tondau, TonCuoi=toncuoi, PhatSinh=phatsinh)
            tempt.save()
    else:
        for item in vtpt:
            toncuoi = item.soluong
            try:
                phatsinh = PhieuNhapVTPT.objects.get(date__year=now.year, date__month=now.month,mavattuphutung=item).soluong
            except:
                phatsinh = 0
            tondau = 0
            tempt = ct_baocaoton(MaBCT=BCT, MaVTPT=item, TonDau=tondau, TonCuoi=toncuoi, PhatSinh=phatsinh)
            tempt.save()
    
    enquiry = ct_baocaoton.objects.all().filter(MaBCT=BCT).order_by('-MaVTPT_id').reverse()
    return render(request, 'gara/baocaoton.html',  {'enquiries': enquiry, 'month': now, 'customer': staff, "picture": picture})

@login_required(login_url="/login")
def baocaoton_luachon(request, username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    context = {'customer': staff, "picture": picture}
    return render(request, 'gara/baocaoton_luachon.html', context)

#-----------------------------------------------------------------------------------------------------------------------------

def update_default():
    QuyDinhHienHanh.objects.create(TenThamSo="So hieu xe", GiaTri = 0)
    QuyDinhHienHanh.objects.create(TenThamSo="So xe sua chua toi da", GiaTri = 0)
    QuyDinhHienHanh.objects.create(TenThamSo="So loai vat tu", GiaTri = 0)
    QuyDinhHienHanh.objects.create(TenThamSo="So loai tien cong", GiaTri = 0)
    QuyDinhHienHanh.objects.create(TenThamSo="Ti le don gia nhap va ban", GiaTri = 1.05)

def regular_update(request, username):
    # enquiries = QuyDinhHienHanh.objects.all().filter()
    a = CapNhatQuyDinh()
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if QuyDinhHienHanh.objects.all().exists() ==False:
        update_default()
    data = QuyDinhHienHanh.objects.all()
    return render(request, 'gara/cap_nhat_quy_dinh.html',{'fa':a, 'data':data, "customer": staff, "picture":picture})


def save_regular_update(request):
    if request.method == 'POST':
        f = CapNhatQuyDinh(request.POST)
        # a = QuyDinhHienHanh.objects.first()
        username = request.user.username
        if f.is_valid():
            f.save()
            print()
            return HttpResponseRedirect(f'{username}/thamso')
        else:
            return HttpResponse("ko co validate")
    else:
        return HttpResponse("not POST request")
        


# def delete_QuyDinh(self):
#     QuyDinhHienHanh.objects.all().delete()

# @user_passes_test(is_admin)
# @login_required(login_url="/login")
def update_quydinh(request , mts, username):
    quy_dinh = QuyDinhHienHanh.objects.get(MaThamSo=mts)
    form = CapNhatQuyDinh(instance= quy_dinh)
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if request.method == 'POST':
        form = CapNhatQuyDinh(request.POST, instance= quy_dinh)
        if form.is_valid():
            form.save()
            return redirect(f'../../{staff.username}/thamso')
    context = {'form':form, "customer": staff, "picture":picture}
    return render(request, 'gara/update_form_qd.html',{'form': form})
    # return render(request, 'gara/update_form.html', context)

def delete_quydinh(request, mts, username):
    staff= Staff.objects.get(username=username)
    quy_dinh = QuyDinhHienHanh.objects.get(MaThamSo=mts)
    if request.method == "POST":
        quy_dinh.delete()
        return HttpResponseRedirect(f'../../{username}/thamso')
    context = {'item': quy_dinh, 'customer': staff}
    return render(request, 'gara/delete_qd.html', context)

#----------------------------------------------------------------------------------------------------------------------------------

def add_ctBaoCaoDoanhSO(request):
    psc_xe = PhieuSuaChua.objects.select_related("maxe__mahieuxe").all()
    hieuxe = HieuXe.objects.all()
    psc_xe.select_related("mahieuxe")
    # maxe_luotsua_thanhtien = psc_xe.values("maxe").annotate(count=Count("maxe")).annotate(Sum=Sum("tongthanhtien"))
    b = psc_xe.values("maxe").annotate(count=Count("maxe")).annotate(Sum=Sum("tongthanhtien"))
    a = hieuxe.values("tenhieuxe","hieuxe")
    for i in range(len(a)):
        print(a[i]['tenhieuxe'], a[i]['hieuxe'])
        sum_hx = 0
        count_hx = 0
        for j in range(len(b)):
            if a[i]['hieuxe'] == b[j]["maxe"]:
                sum_hx += b[j]["Sum"]
                count_hx += b[j]["Sum"]
        CT_BaoCaoDoanhSO.objects.create(mahieuxe= a[i]['hieuxe'], luotsua=sum_hx,thanhtien=count_hx)
    return 0

def data_xe_hieuxe_psc():
    x = Xe.objects.all()
    hx = HieuXe.objects.all()
    psc = PhieuSuaChua.objects.all()
    df_x = pd.DataFrame(x.values())
    df_hx = pd.DataFrame(hx.values())
    df_psc = pd.DataFrame(psc.values())
    df_xhx = df_x.join(df_hx.set_index("mahieuxe"), on = "mahieuxe_id")
    df = df_psc.join(df_xhx.set_index("maxe"), on = "maxe_id")

    # df['ngaytiepnhan'] = pd.to_datetime(df['ngaytiepnhan'])
    # df['ngaytiepnhan'].dt.to_period('M')

    df['ngaylapphieu'] = pd.to_datetime(df['ngaylapphieu'])
    df['thanglapphieu']=df['ngaylapphieu'].dt.to_period('M')
    df['month'] = df['ngaylapphieu'].dt.month
    df['year'] = df['ngaylapphieu'].dt.year


    ct_ds = df.groupby(["month","year","tenhieuxe"])['tongthanhtien'].agg(['sum','count']).reset_index()
    total = df.groupby(["month","year"])['tongthanhtien'].agg(['sum','count']).reset_index()
    data = pd.merge(ct_ds,total, how="left", on=['month','year']) #col: ['month', 'year', 'tenhieuxe', 'sum', 'count_x', 'count_y'],
    data['tile']=data['count_x']/data['count_y']*100
    return data

def Bao_Cao_Doanh_So(request, username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    CT_BaoCaoDoanhSO.objects.all().delete()
    BaoCaoDoanhSo.objects.all().delete()
    x = Xe.objects.all()
    hx = HieuXe.objects.all()
    psc = PhieuSuaChua.objects.all()
    df_x = pd.DataFrame(x.values())
    df_hx = pd.DataFrame(hx.values())
    df_psc = pd.DataFrame(psc.values())
    df_xhx = df_x.join(df_hx.set_index("mahieuxe"), on = "mahieuxe_id")
    df = df_psc.join(df_xhx.set_index("maxe"), on = "maxe_id")

    # df['ngaytiepnhan'] = pd.to_datetime(df['ngaytiepnhan'])
    # df['ngaytiepnhan'].dt.to_period('M')

    df['ngaylapphieu'] = pd.to_datetime(df['ngaylapphieu'])
    df['thanglapphieu']=df['ngaylapphieu'].dt.to_period('M')
    df['month'] = df['ngaylapphieu'].dt.month
    df['year'] = df['ngaylapphieu'].dt.year

    ct_ds = df.groupby(["month","year","tenhieuxe"])['tongthanhtien'].agg(['sum','count']).reset_index()
    total = df.groupby(["month","year"])['tongthanhtien'].agg(['sum','count']).reset_index()
    data = pd.merge(ct_ds,total, how="left", on=['month','year']) #col: ['month', 'year', 'tenhieuxe', 'sum', 'count_x', 'count_y'],
    data['tile']=data['count_x']/data['count_y']*100
    # data= data_xe_hieuxe_psc()
    for tenhieuxe, luotsua, thanhtien, ti_le, stt  in zip(data['tenhieuxe'], data['count_x'], data['sum_x'], data['tile'], data.index):
        CT_BaoCaoDoanhSO.objects.create(tenhieuxe=tenhieuxe,luotsua=luotsua,thanhtien=thanhtien,ti_le=ti_le,STT = stt)

    # ===============================================================
    for month, year, tongdoanhso in zip(total['month'],total['year'],total['sum']):
        BaoCaoDoanhSo.objects.create(month =month,year = year, tongdoanhso= tongdoanhso)

    if BaoCaoDoanhSo.objects.all().exists() ==False:
        return HttpResponse("update that bai")

    if CT_BaoCaoDoanhSO.objects.all().exists() ==False:
        return HttpResponse("update that bai")

    bcds = BaoCaoDoanhSo.objects.all()
    ct_bcds = CT_BaoCaoDoanhSO.objects.all()
    context={"bcds":bcds,"ct_bcds":ct_bcds, "customer": staff, "picture":picture}
    return render(request, 'gara/bao_cao_doanh_thu.html',context)

            

def search_bcds(request, username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if 'm'and'y' in request.GET:
        m = request.GET['m']
        y = request.GET['y']
        data = data_xe_hieuxe_psc()
        try:
            bcds = BaoCaoDoanhSo.objects.filter(month = m, year = y)
            search_ct_bcds = data.loc[(data['month']==int(m)) & (data['year']==int(y))]  
        except:
            try:
                if y=='':
                    bcds = BaoCaoDoanhSo.objects.filter(month = m)
                    search_ct_bcds = data.loc[(data['month']==int(m))]
                if m=='':
                    bcds = BaoCaoDoanhSo.objects.filter(year = y)
                    search_ct_bcds = data.loc[(data['year']==int(y))]
            except:
                bcds = BaoCaoDoanhSo.objects.all()
                search_ct_bcds = data
        
        b = search_ct_bcds.index
        ct_bcds = CT_BaoCaoDoanhSO.objects.filter(STT__in = list(b)) 
    else:
        bcds = BaoCaoDoanhSo.objects.all()
        ct_bcds = CT_BaoCaoDoanhSO.objects.all()
    context={"bcds":bcds, "ct_bcds":ct_bcds, "customer": staff, "picture":picture}
    return render(request, 'gara/bao_cao_doanh_thu.html',context)

def nhap_vtpt(request, username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    enquiry=NhapCTVatTuPhuTung()
    if request.method=='POST':
        enquiry=NhapCTVatTuPhuTung(request.POST)
        if enquiry.is_valid():
            try:
                vtpt = VatTuPhuTung.objects.get(tenvattuphutung=request.POST['tenvattuphutung'])
            except:
                vtpt= False

            if vtpt:
                vtpt.dongia=request.POST['dongia']
                vtpt.soluong+=int(request.POST['soluong'])
                vtpt.save()
            else:
                if VatTuPhuTung.objects.all().count() < QuyDinhHienHanh.objects.get(TenThamSo='So loai vat tu').GiaTri:
                    vtpt = VatTuPhuTung(tenvattuphutung=request.POST['tenvattuphutung'], dongia=request.POST['dongia'], soluong=request.POST['soluong'])
                    vtpt.save()
                    messages.success(request, 'Nhập thành công')
                else:
                    return HttpResponse('Quá số lượng tối đa vật tư phụ tùng')
            phieu = PhieuNhapVTPT(mavattuphutung=vtpt,soluong=vtpt.soluong,dongia=vtpt.dongia)
            phieu.save()
            return HttpResponseRedirect('nhap_vtpt')
    
    return render(request,'phieunhapvtpt/nhapphutung.html',{'enquiry':enquiry, 'customer':staff, 'picture':picture})

def them_hieuxe(request, username):
    enquiry=ThemHieuXe
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if request.method=='POST':
        enquiry=ThemHieuXe(request.POST)
        print('POST is method')
        if enquiry.is_valid():
            print('enquiry is valid')
            tenhieuxe=request.POST['tenhieuxe']
            soluonghieuxe=HieuXe.objects.all().count()
            print('soluonghieuxe la', soluonghieuxe)
            max=QuyDinhHienHanh.objects.get(TenThamSo='So hieu xe').GiaTri
            if soluonghieuxe>max:
                messages.warning(request,f'so luong hieu xe qua {max}')
                return HttpResponseRedirect('nhap_hieuxe')
            else:    
                HieuXe.objects.create(tenhieuxe=tenhieuxe)
                messages.success(request, 'Nhập hiệu xe thành công')
                return HttpResponseRedirect('nhap_hieuxe')
    context={'enquiry':enquiry, 'customer':staff, 'picture':picture}
    return render(request,'bonus/themhieuxe.html',context)

def them_tiencong(request, username):
    print('Hello')
    enquiry=ThemTienCong
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    if request.method=='POST':
        enquiry=ThemTienCong(request.POST)
        print('POST is method')
        if enquiry.is_valid():
            print('enquiry is valid')
            loaitiencong=request.POST['loaitiencong']
            soluongtiencong=TienCong.objects.all().count()
            print('soluongtiencong la', soluongtiencong)
            max = QuyDinhHienHanh.objects.get(TenThamSo='So loai tien cong').GiaTri
            if soluongtiencong>QuyDinhHienHanh.objects.get(TenThamSo='So loai tien cong').GiaTri:
                messages.warning(request,f'số lượng không được vượt quá {max}')
            else:    
                TienCong.objects.create(loaitiencong=loaitiencong,tiencong=request.POST['tiencong'])
                messages.success(request, 'Thêm tiền công thành công')
    context={'enquiry':enquiry, 'customer':staff, 'picture':picture}
    return render(request,'bonus/themtiencong.html',context)

def get_bd(request,username):
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    x = Xe.objects.all()
    hx = HieuXe.objects.all()
    kh = KhachHang.objects.all()
    df_x = pd.DataFrame(x.values())
    df_hx = pd.DataFrame(hx.values())
    df_kh = pd.DataFrame(kh.values())
    df_xhx = df_x.join(df_hx.set_index("mahieuxe"), on = "mahieuxe_id")
    data = df_xhx.join(df_kh.set_index("makhachhang"), on = "makhachhang_id")    
    df = data[["bienso","tenhieuxe","tenkhachhang","tienno"]]
    return render(request, 'gara/search_xe.html', {'df':df, 'customer':staff, 'picture':picture})

def data_tracuuxe():
    x = Xe.objects.all()
    hx = HieuXe.objects.all()
    kh = KhachHang.objects.all()
    df_x = pd.DataFrame(x.values())
    df_hx = pd.DataFrame(hx.values())
    df_kh = pd.DataFrame(kh.values())
    df_xhx = df_x.join(df_hx.set_index("mahieuxe"), on = "mahieuxe_id")
    data = df_xhx.join(df_kh.set_index("makhachhang"), on = "makhachhang_id")
    return data
    
def after_search(request, username):
    data = data_tracuuxe()
    staff = Staff.objects.get(username=username)
    picture = '../' + staff.profile_pic.url
    # if "tukhoa" and "bienso" and "baocao" in request.GET:
    if  "bienso"  in request.GET:
        kh = request.GET['khachhang']
        bs = request.GET['bienso']
        hx = request.GET['hieuxe']
        print("=======: ",kh == '' , hx == '' )
        
        if kh == '' and hx == '':
            a = data.loc[(data["bienso"].str.contains(bs))]
        elif bs == '' and kh == '':
            a = data.loc[(data["tenhieuxe"].str.contains(hx))]
        elif bs == '' and hx == '':
            a = data.loc[(data["tenkhachhang"].str.contains(kh))]
        elif hx == '':
            a = data.loc[(data["bienso"].str.contains(bs)) & (data["tenkhachhang"].str.contains(kh)) ]
        elif bs == '':
            a = data.loc[(data["tenhieuxe"].str.contains(hx)) & (data["tenkhachhang"].str.contains(kh)) ]
        elif kh == '':
            a = data.loc[(data["tenhieuxe"].str.contains(hx)) & (data["bienso"].str.contains(bs)) ]
        else:
            a = data.loc[(data["tenhieuxe"].str.contains(hx)) & (data["bienso"].str.contains(bs)) & (data["tenkhachhang"].str.contains(kh)) ]
        df = a[["bienso","tenhieuxe","tenkhachhang","tienno"]]
    else:             
        df = data[["bienso","tenhieuxe","tenkhachhang","tienno"]]
    return render(request, 'gara/search_xe.html', {'df':df, 'customer':staff, 'picture':picture})