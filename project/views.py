from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Project, Progress, Task, Vision
import xlrd, xlwt
from django.db import transaction

# Create your views here.


'''
def paginate_template(self):
    total_date = self.objects.count()  # 获取数据总量
    show_date = []
    if total_date == 0:
        context = {
            'show_date': '暂无数据',
        }
    else:
        va, remain = divmod(total_date, 10)
        if remain:
            va += 1  # 如果有余数，页数加1
        if va == 1:  # 只有一页，显示所有数据
            show_date = self.objects.all()
        else:
            for i in range(0, va):
                if i < va - 1:  # 如果不是最后一页
                    show_date.append(self.objects.all()[i * 10:10 * i + 9])
                else:  # 最后一页数据
                    show_date.append(self.objects.all()[va * 10:])
        context = {'show_date': show_date}
    return context

'''

def product(request):
    del_id = request.GET.get('del_id')
    page = request.GET.get('page')

    #删除数据
    if del_id:
        Product.objects.get(id=del_id).delete()
        #删完数据重定向到当前页
        red_path = '?page='+str(page)
        return HttpResponseRedirect(reverse('project:product')+red_path)
    else:
        # 分页
        product_list = Product.objects.all()
        # 按每页10条数据分页
        paginator = Paginator(product_list, 10)
        try:
            product_date = paginator.page(page)
        # 显示第一页,传入page的值为None或空
        except PageNotAnInteger:
            product_date = paginator.page(1)
        # 传入page值不在有效范围
        except EmptyPage:
            product_date = paginator.page(paginator.num_pages)
        context = {'product_date': product_date}

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
def product_add():
    return HttpResponseRedirect(reverse('project:product'))