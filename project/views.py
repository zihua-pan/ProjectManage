from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Project, Progress, Task, Vision
import xlrd, xlwt
from django.db import transaction

# Create your views here.


def product(request):
    del_id = request.GET.get('del_id')
    page = request.GET.get('page', 1)

    #删除数据
    if del_id:
        Product.objects.get(id=del_id).delete()
        #删完数据重定向到当前页
        red_path = '?page='+str(page)
        return HttpResponseRedirect(reverse('project:product')+red_path)
    else:
        # 分页
        product_list = Product.objects.all()
        # 按每页count_page条数据分页
        count_page =10
        paginator = Paginator(product_list, count_page)
        start = (int(page)-1)*count_page
        try:
            product_date = paginator.page(page)
        # 显示第一页,传入page的值为None或空
        except PageNotAnInteger:
            product_date = paginator.page(1)
        # 传入page值不在有效范围
        except EmptyPage:
            product_date = paginator.page(paginator.num_pages)
        context = {
            'product_date': product_date,
            'start': start
        }

    #导入数据
    if request.method == 'POST':
        product_file = request.FILES.get('product_file')
        file_type = product_file.name.split('.')[1]
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=product_file.read())
            tables = data.sheets()
            for table in tables:
                rows = table.nrows
                try:
                    with transaction.atomic():
                        data_table = []
                        for row in range(1, rows):
                            row_values = table.row_values(row)
                            data_table.append(Product(
                                pd_model=row_values[0],
                                pd_type=row_values[1],
                                pd_name=row_values[2],
                            ))
                        Product.objects.bulk_create(data_table)
                except Exception:
                    print('解析excel文件或者数据插入错误！')
            print('数据导入成功')
        else:
            print('上传文件类型错误！')
    return render(request, 'project/product.html', context)

#导出产品数据
def download(request):
    data_table = []
    product_set = list(Product.objects.all().order_by('id'))
    for item in product_set:
        data_table.append([item.pd_model, item.pd_type, item.pd_name])
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('产品数据')
    worksheet.write(0, 0, '产品型号')
    worksheet.write(0, 1, '产品类型')
    worksheet.write(0, 2, '产品名称')
    i = 1
    for data in data_table:
        worksheet.write(i,0,data[0])
        worksheet.write(i,1,data[1])
        worksheet.write(i,2,data[2])
        i += 1
    workbook.save(r'C:\Users\Master\Desktop\test.xlsx')
    return render(request, 'project/task.html')



def project(request):
    if Project.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        context = {
            'projectset': list(Project.objects.all()),
        }
    return render(request, 'project/project.html', context)


def task(request):
    if Task.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        context = {
            'taskset': list(Task.objects.all()),
        }
    return render(request, 'project/task.html', context)


def vision(request):
    if Vision.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        context = {
            'visionset': list(Vision.objects.all()),
        }
    return render(request, 'project/vision.html', context)


def progress(request):
    if Progress.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        context = {
            'progressset': list(Progress.objects.all()),
        }
    return render(request, 'project/progress.html', context)


#手动添加一条产品数据
def product_add(request):
    if request.method == 'GET':
        return render(request, 'project/product.html')

    elif request.method == 'POST':
        pd_model = request.POST.get('pd_model')
        pd_type = request.POST.get('pd_type')
        pd_name = request.POST.get('pd_name')
        context = {}
        try:
            #判断产品型号是否存在
            Product.objects.get(pd_model=pd_model)
            #产品型号不存在
        except Product.DoesNotExist:
            Product.objects.create(pd_model=pd_model, pd_type=pd_type, pd_name=pd_name)
        else:
            context = {'wrong': '产品型号已存在'}
        return render(request, 'project/product.html', context)