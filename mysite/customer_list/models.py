from argparse import HelpFormatter
from multiprocessing import managers
from statistics import mode
from django.db import models


# Create your models here.

class Customer_Info(models.Model):
    """입소자 정보 테이블: 기초 정보를 기준으로 나중에 뻣어 나갈 수 있게, 또한 상태에 따라 이용하는 페이지나 테이블 연동이 서로간에 유기적으로
    연결될 수 있도록 함"""

    
    CUSTOMER_STATUS = (
        ('c','계속'),
        ('o','퇴소'),
        ('i','입소'),
        ('s','외박'),
        ('r','복귀'),
    )

    Customer_Idx = models.AutoField(primary_key=True, help_text='입소자 고유번호')
    Customer_Name = models.CharField(max_length=30, help_text='입소자명')
    Customer_Barnchcode = models.SmallIntegerField(default=0, help_text='소속지점 번호')
    Customer_Status = models.SmallIntegerField(default=0, help_text='입소자 상태')

    #생년월일 / 음력생일 분리
    Customer_Birth = models.DateField('date pulished', help_text='입소자 생년월일')
    Customer_Lunarbirth = models.DateField('date pulished', null=True, blank=True, help_text='생신')
    Customer_Sex = models.SmallIntegerField(default=1, help_text='성별')
    Customer_Address = models.TextField(max_length=200, help_text='주소')
    class Meta:
        ordering = ['Customer_Name']

    def __str__(self):
        return self.Customer_Name

class Customer_LongtermInfo(models.Model):
    """입소자의 장기요양 정보 테이블 - 기초 정보 테이블과 연동해서 사용한다"""

    Idx = models.ForeignKey(Customer_Info, on_delete=models.CASCADE)

    # 장기요양 번호 장기요양 등급
    Longterm_Number = models.IntegerField(null=True, blank=True)
    Longterm_Rank = models.SmallIntegerField(null=True, blank=True)
    # 건보 등급
    Healthinsurance_Rank = models.SmallIntegerField(null=True, blank=True)
    # 장기요양 등급 인정일(시작/종료)
    Longterm_Startdate = models.DateField('date pulished')
    Longterm_Enddate = models.DateField('date pulished')
    def __str__(self):
        return self.Longterm_Number


    



    

    