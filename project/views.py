from django.shortcuts import render
from .models import Product, Project, Progress, Task, Vision
import xlrd, xlwt
from django.db import transaction

# Create your views here.


def product(request):
    if Product.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        context = {
            'productset': list(Product.objects.all()),
        }
        #导出数据
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


def delete(request):

    return render(request, 'project/product.html')


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
