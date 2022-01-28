from json import load
import select
from django import http
from django import template
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import json

from openpyxl import load_workbook

import customer_list

# Create your views here.
from .models import Customer_Info

# 기본 페이지 뷰
def index(request):
    latest_customer_list = Customer_Info.objects.order_by('Customer_Idx')[:5]
    context = {'latest_customer_list': latest_customer_list}
    return render(request, 'customer_list/index.html', context)

# 사용자 정보 수정 뷰
def modify(request, Customer_Idx):    
    """값을 선택해서 수정페이지로 온다. 해당 페이지에서 수정하고 싶은 값을 설정하고 액션으로 넘겨서 DB에 쓰고자 함"""
    latest_customer_list = Customer_Info.objects.get(pk=Customer_Idx)
    context = {'latest_customer_list': latest_customer_list}
    # return render(request, 'customer_list/'+str(Customer_Idx)+'/modify.html', context)
    return render(request, 'customer_list/modify.html', context)

# 사용자 정보 수정 뷰(액션)
def modify_action(request, Customer_Idx):
    """입소자의 고유값을 받아와서 해당 값을 덮어 쓴다. 약간 원시적인 코드"""
    modify_value = get_object_or_404(Customer_Info, pk=Customer_Idx)
    modify_value.Customer_Name = request.POST['c_name']
    modify_value.Customer_Barnchcode = request.POST['c_branch']
    modify_value.Customer_Address = request.POST['c_address']
    modify_value.Customer_Birth = request.POST['c_birth']
    modify_value.Customer_Sex = request.POST['c_sex']
    modify_value.Customer_Status = request.POST['c_status']
    modify_value.save()
    return render(request, 'customer_list/index.html', context=None)

# 사용자 정보 생성 뷰
def create(request):
    """입소자 신규 생성 페이지 뷰"""
    return render(request, 'customer_list/create.html', context=None)

# 사용자 정보 생성 뷰(액션)
def create_action(request):
    """입소자 신규 생성 액션 뷰"""
    new_value = Customer_Info()
    new_value.Customer_Name = request.POST['c_name']
    new_value.Customer_Barnchcode = request.POST['c_branch']
    new_value.Customer_Address = request.POST['c_address']
    new_value.Customer_Birth = request.POST['c_birth']
    new_value.Customer_Sex = request.POST['c_sex']
    new_value.Customer_Status = request.POST['c_status']
    new_value.save()
    return render(request, 'customer_list/index.html', context=None)
    


# 여기서 부터 외부 소스
# 엑셀 업로드 뷰(외부 퍼옴)
def salary_update_excel(request):
    if request.method == 'POST':

        # 파일 저장
        # file = request.FILES['file_excel']
        # fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)

        file = request.FILES['file_excel']
        
        # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
        load_wb = load_workbook(file, data_only=True)
        
        # 시트 이름으로 불러오기
        load_ws = load_wb['Sheet1']

        # 셀 주소로 값 출력
        # print(load_ws['A1'].value)

        # 일단 리스트에 담기
        all_values = []
        for row in load_ws.rows:
            row_value = []
            for cell in row:
                row_value.append(cell.value)
            all_values.append(row_value)

        cnt = 0
        for idx, val in enumerate(all_values):
            if idx == 0:
                #엑셀 형식 체크 (첫번째의 제목 row)
                if val[0]!='항목1' or val[1]!='항목2' or val[2]!='항목3':
                    context = {'state': False, 'rtnmsg': '엑셀 항목이 올바르지 않습니다.'}
                    return HttpResponse(json.dumps(context), content_type="application/json")
            else:
                # print(type(val[2]))
                if val[2] and type(val[2]) == int :
                    memData = Customer_Info.objects.get(msabun=val[0], mname=val[1])
                    memData.myear_salary = val[2]
                    memData.save()
                    cnt += 1


        context = {'state': True, 'rtnmsg' : '{0}건의 엑셀 데이터가 반영 되었습니다.'.format(cnt)}
        return HttpResponse(json.dumps(context), content_type="application/json")

# Ajax 테스트용 뷰
def test(request):
    jsonObject = json.loads(request.body)
    print(jsonObject.get('title'))
    return JsonResponse(jsonObject)