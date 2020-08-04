from io import BytesIO
import xlwt
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from my_tools.my_utils import export, template
from .models import *
import xlrd
from django.db import transaction





# 项目视图
def project(request):
    del_id = request.GET.get('del_id', '')
    page = request.GET.get('page', 1)
    search_data = request.GET.get('search', '')
    if del_id:  # 删除数据
        Project.objects.get(project_num=del_id).delete()
        # 删完数据重定向到当前页
        red_path = '?page=' + str(page)
        return HttpResponseRedirect(reverse('project:project') + red_path)
    if search_data:  # 根据项目编号或名称查询
        project_list = Project.objects.filter(
            Q(project_num__contains=search_data) | Q(project_name__contains=search_data)
        )
    else:
        project_list = Project.objects.all()  # 查询全部数据
    count_page = 10     # 按每页count_page条数据分页
    paginator = Paginator(project_list, count_page)
    start = (int(page) - 1) * count_page  # 每页起始数据编号
    try:
        project_data = paginator.page(page)
    except PageNotAnInteger:  # 显示第一页,传入page的值为None或空，默认为1
        project_data = paginator.page(1)
    except EmptyPage:           # 传入page值不在有效范围
        project_data = paginator.page(paginator.num_pages)
    context = {
        'project_data': project_data,
        'start': start,
        'search_data': search_data,
        'username': request.user,
    }
    return render(request, 'project/project.html', context)


# 导入项目数据
def project_import(request):
    if request.method == 'POST':
        project_file = request.FILES.get('project_file')
        file_type = project_file.name.split('.')[1]  # 获取文件后缀
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=project_file.read())
            tables = data.sheets()
            for table in tables:  # 遍历工作表
                rows = table.nrows  # 获取sheet中的有效行数
                try:
                    with transaction.atomic():  # 事务管理
                        data_table = []
                        for row in range(1, rows):
                            row_values = table.row_values(row)  # 获取本行数据
                            data_table.append(Project(
                                project_num=row_values[0],
                                project_name=row_values[1],
                                project_manager=row_values[2],
                            ))
                        Project.objects.bulk_create(data_table)  # 批量插入数据
                except Exception:
                    return HttpResponse('解析excel文件或者数据插入错误！')
            return HttpResponse('数据导入成功')
        else:
            return HttpResponse('上传文件类型错误！')
    return render(request, 'project/product.html')






# 导出项目数据
def project_download(request, model):
    sio = BytesIO()
    if model == 1:  # 模式1，导出数据
        export(Project).save(sio)
    elif model == 2:  # 模式2，导出模板
        template(Project).save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    response.write(sio.getvalue())
    return response


# 修改项目数据
def project_modify(request):
    project_num = request.POST.get('project_num')
    project_name = request.POST.get('project_name')
    project_manager = request.POST.get('project_manager')
    department = request.POST.get('department')
    try:
        pj = Project.objects.get(project_num=project_num)
    except Product.DoesNotExist:
        return HttpResponse('项目不存在')
    else:
        pj.project_name = project_name
        pj.project_manager = project_manager
        pj.to_department
        pj.save()
        return HttpResponseRedirect(reverse('project:project'))


# 添加项目数据
def project_add(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'project/project.html')

    if request.method == 'POST':
        project_num = request.POST.get('project_num')
        project_name = request.POST.get('project_name')
        project_manager = request.POST.get('project_manager')
        department = request.POST.get('department')
        try:
            Project.objects.get(project_num=project_num)  # 判断项目是否存在
        except Project.DoesNotExist:  # 创建新项目
            try:
                pd = Department.objects.get(department_name=department)  # 判断事业部是否存在
            except Department.DoesNotExist:
                Project.objects.create(
                    project_num=project_num,
                    project_name=project_name,
                    project_manager=project_manager,).to_department.create(department_name=department)
            else:
                Project.objects.create(
                    project_num=project_num,
                    project_name=project_name,
                    project_manager=project_manager,).to_department.add(pd)
                return HttpResponseRedirect(reverse('project:project'))
        else:
            context['wrong'] = '已存在该项目'
    return render(request, 'project/project.html', context)







# 产品视图
@login_required
def product(request):
    del_id = request.GET.get('del_id', '')
    page = request.GET.get('page', 1)
    search_data = request.GET.get('search', '')
    if del_id:     # 删除数据
        Product.objects.get(product_model=del_id).delete()
        # 删完数据重定向到当前页
        red_path = '?page='+str(page)
        return HttpResponseRedirect(reverse('project:product')+red_path)
    if search_data:   # 模糊查询
        product_list = Product.objects.filter(
            Q(product_model__contains=search_data)|Q(product_name__contains=search_data)
        )
    else:
        product_list = Product.objects.all()    # 查询全部数据
    count_page =10    # 按每页count_page条数据分页
    paginator = Paginator(product_list, count_page)
    start = (int(page)-1)*count_page
    try:
        product_data = paginator.page(page)
    # 显示第一页,传入page的值为None或空，默认为1
    except PageNotAnInteger:
        product_data = paginator.page(1)
    # 传入page值不在有效范围
    except EmptyPage:
        product_data = paginator.page(paginator.num_pages)
    context = {
        'product_data': product_data,
        'start': start,
        'search_data': search_data,
        'username': request.user,
    }
    return render(request, 'project/product.html', context)


# 导入产品数据
def product_import(request):
    if request.method == 'POST':
        product_file = request.FILES.get('product_file')
        file_type = product_file.name.split('.')[1]  # 获取文件后缀
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
                            try:
                                projects = Project.objects.get(project_num=row_values[3]) # 判断项目是否存在
                            except Project.DoesNotExist:
                                return HttpResponse('数据中有未被创建的项目！')
                            else:
                                data_table.append(Product(
                                    product_model=row_values[0],
                                    product_type=row_values[1],
                                    product_name=row_values[2],
                                    projects=projects,
                                ))
                        Product.objects.bulk_create(data_table)
                except Exception:
                    return HttpResponse('解析excel文件或者数据插入错误！')
            return HttpResponse('数据导入成功')
        else:
            return HttpResponse('上传文件类型错误！')
    return render(request, 'project/product.html')


# 导出产品数据
def product_download(request, model):
    sio = BytesIO()
    if model == 1:  # 模式1，导出数据
        export(Product).save(sio)
    elif model == 2:  # 模式2，导出模板
        template(Product).save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    response.write(sio.getvalue())
    return response


# 添加一条产品数据
def product_add(request):
    if request.method == 'GET':
        return render(request, 'project/product.html')

    if request.method == 'POST':
        project_num = request.POST.get('project_num')
        product_model = request.POST.get('product_model')
        product_type = request.POST.get('product_type')
        product_name = request.POST.get('product_name')
        context = {}
        try:
            projects = Project.objects.get(project_num=project_num)  # 判断项目是否存在
        except Project.DoesNotExist:
            context['wrong'] = '该项目不存在'
        else:
            try:
                Product.objects.get(product_model=product_model)  # 判断产品型号是否存在
            except Product.DoesNotExist:
                Product.objects.create(
                    projects=projects,
                    product_model=product_model,
                    product_type=product_type,
                    product_name=product_name,)
                return HttpResponseRedirect(reverse('project:product'))
            else:
                context = {'wrong': '产品型号已存在'}
        return render(request, 'project/product.html', context)


# 修改产品数据
def product_modify(request):
    product_model = request.POST.get('product_model')
    product_type = request.POST.get('product_type')
    product_name = request.POST.get('product_name')
    try:
        pd = Product.objects.get(product_model=product_model)
    except Product.DoesNotExist:
        return HttpResponse('产品不存在')
    else:
        pd.product_type = product_type
        pd.product_name = product_name
        pd.save()
        return HttpResponseRedirect(reverse('project:product'))



# 任务视图
@login_required
def task(request):
    del_id = request.GET.get('del_id', '')
    page = request.GET.get('page', 1)
    search_data = request.GET.get('search', '')
    if del_id:     # 删除数据
        Task.objects.get(task_num=del_id).delete()
        # 删完数据重定向到当前页
        red_path = '?page='+str(page)
        return HttpResponseRedirect(reverse('project:task')+red_path)
    if search_data:   # 模糊查询
        task_list = Task.objects.filter(task_num=search_data)
    else:
        task_list = Task.objects.all()    # 查询全部数据
    count_page =10    # 按每页count_page条数据分页
    paginator = Paginator(task_list, count_page)
    start = (int(page)-1)*count_page
    try:
        task_data = paginator.page(page)
    # 显示第一页,传入page的值为None或空，默认为1
    except PageNotAnInteger:
        task_data = paginator.page(1)
    # 传入page值不在有效范围
    except EmptyPage:
        task_data = paginator.page(paginator.num_pages)
    context = {
        'task_data': task_data,
        'start': start,
        'search_data': search_data,
        'username': request.user,
    }
    return render(request, 'project/task.html', context)


# 导入任务数据
def task_import(request):
    if request.method == 'POST':
        task_file = request.FILES.get('task_file')
        file_type = task_file.name.split('.')[1]  # 获取文件后缀
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=task_file.read())
            tables = data.sheets()
            for table in tables:
                rows = table.nrows
                try:
                    with transaction.atomic():
                        data_table = []
                        for row in range(1, rows):
                            row_values = table.row_values(row)
                            try:
                                products = Product.objects.get(product_model=row_values[1])  # 判断产品是否存在
                            except Product.DoesNotExist:
                                return HttpResponse('数据中有不存在的产品！')
                            else:
                                data_table.append(Task(
                                    task_num=row_values[0],
                                    products=products,
                                    dev_type=row_values[2],
                                    start_time=row_values[3],
                                    end_time=row_values[4],
                                    task_status=row_values[5],
                                ))
                        task.objects.bulk_create(data_table)
                except Exception:
                    return HttpResponse('解析excel文件或者数据插入错误！')
            return HttpResponse('数据导入成功')
        else:
            return HttpResponse('上传文件类型错误！')
    return render(request, 'project/task.html')


# 导出任务数据
def task_download(request, model):
    sio = BytesIO()
    if model == 1:  # 模式1，导出数据
        export(Task).save(sio)
    elif model == 2:  # 模式2，导出模板
        template(Task).save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    response.write(sio.getvalue())
    return response


# 添加一条任务数据
def task_add(request):
    if request.method == 'GET':
        return render(request, 'project/task.html')

    if request.method == 'POST':
        task_num = request.POST.get('task_num')
        product_model = request.POST.get('product_model')
        dev_type = request.POST.get('dev_type')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        task_status = request.POST.get('task_status')
        context = {}
        try:
            products = Product.objects.get(product_model=product_model)  # 判断产品是否存在
        except Product.DoesNotExist:
            context['wrong'] = '该项目不存在'
        else:
            Task.objects.create(
                task_num=task_num,
                products=products,
                dev_type=dev_type,
                start_time=start_time,
                end_time=end_time,
                task_status=task_status,)
            return HttpResponseRedirect(reverse('project:task'))
        return render(request, 'project/task.html', context)


# 修改任务数据
def task_modify(request):
    task_num = request.POST.get('task_num')
    dev_type = request.POST.get('dev_type')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    task_status = request.POST.get('task_status')
    try:
        tk = Task.objects.get(task_num=task_num)
    except Task.DoesNotExist:
        return HttpResponse('任务不存在')
    else:
        tk.dev_type = dev_type
        tk.start_time = start_time
        tk.end_time = end_time
        tk.task_status = task_status
        tk.save()
        return HttpResponseRedirect(reverse('project:task'))





# 版本视图
@login_required
def vision(request):
    del_id = request.GET.get('del_id', '')
    page = request.GET.get('page', 1)
    search_data = request.GET.get('search', '')
    if del_id:     # 删除数据
        Vision.objects.get(vision_name=del_id).delete()
        # 删完数据重定向到当前页
        red_path = '?page='+str(page)
        return HttpResponseRedirect(reverse('project:vision')+red_path)
    if search_data:   # 模糊查询
        vision_list = Vision.objects.filter(vision_name=search_data)
    else:
        vision_list = Vision.objects.all()    # 查询全部数据
    count_page =10    # 按每页count_page条数据分页
    paginator = Paginator(vision_list, count_page)
    start = (int(page)-1)*count_page
    try:
        vision_data = paginator.page(page)
    # 显示第一页,传入page的值为None或空，默认为1
    except PageNotAnInteger:
        vision_data = paginator.page(1)
    # 传入page值不在有效范围
    except EmptyPage:
        vision_data = paginator.page(paginator.num_pages)
    context = {
        'vision_data': vision_data,
        'start': start,
        'search_data': search_data,
        'username': request.user,
    }
    return render(request, 'project/vision.html', context)


# 导入版本数据
def vision_import(request):
    if request.method == 'POST':
        vision_file = request.FILES.get('vision_file')
        file_type = vision_file.name.split('.')[1]  # 获取文件后缀
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=vision_file.read())
            tables = data.sheets()
            for table in tables:
                rows = table.nrows
                try:
                    with transaction.atomic():
                        data_table = []
                        for row in range(1, rows):
                            row_values = table.row_values(row)
                            try:
                                tasks = Task.objects.get(task_num=row_values[1])  # 判断任务是否存在
                            except Task.DoesNotExist:
                                return HttpResponse('数据中有不存在的任务！')
                            else:
                                data_table.append(Vision(
                                    vision_num=row_values[0],
                                    vision_name=row_values[1],
                                    executor=row_values[2],
                                    start_time=row_values[3],
                                    end_time=row_values[4],
                                ))
                        Vision.objects.bulk_create(data_table)
                except Exception:
                    return HttpResponse('解析excel文件或者数据插入错误！')
            return HttpResponse('数据导入成功')
        else:
            return HttpResponse('上传文件类型错误！')
    return render(request, 'project/vision.html')


# 导出版本数据
def vision_download(request, model):
    sio = BytesIO()
    if model == 1:  # 模式1，导出数据
        export(Vision).save(sio)
    elif model == 2:  # 模式2，导出模板
        template(Vision).save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    response.write(sio.getvalue())
    return response


# 添加一条版本数据
def vision_add(request):
    if request.method == 'GET':
        return render(request, 'project/vision.html')

    if request.method == 'POST':
        vision_num = request.POST.get('vision_num')
        vision_name = request.POST.get('vision_name')
        executor = request.POST.get('executor')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        task_num = request.POST.get('task_num')
        context = {}
        try:
            tasks = Task.objects.get(task_num=task_num)  # 判断任务是否存在
        except Task.DoesNotExist:
            context['wrong'] = '该任务不存在'
        else:
            Vision.objects.create(
                tasks=tasks,
                vision_num=vision_num,
                vision_name=vision_name,
                executor=executor,
                start_time=start_time,
                end_time=end_time,)
            return HttpResponseRedirect(reverse('project:vision'))
        return render(request, 'project/vision.html', context)


# 修改版本数据
def vision_modify(request):
    vision_name = request.POST.get('vision_name')
    executor = request.POST.get('executor')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    try:
        vs = Vision.objects.get(vision_name=vision_name)
    except Vision.DoesNotExist:
        return HttpResponse('该版本不存在')
    else:
        vs.executor = executor
        vs.start_time = start_time
        vs.end_time = end_time
        vs.save()
        return HttpResponseRedirect(reverse('project:vision'))



# 进度视图
@login_required
def progress(request):
    del_id = request.GET.get('del_id', '')
    page = request.GET.get('page', 1)
    search_data = request.GET.get('search', '')
    if del_id:     # 删除数据
        Progress.objects.get(id=del_id).delete()
        # 删完数据重定向到当前页
        red_path = '?page='+str(page)
        return HttpResponseRedirect(reverse('project:progress')+red_path)
    if search_data:   # 模糊查询
        progress_list = Task.objects.get(task_num=search_data).to_progress.all()
    else:
        progress_list = Progress.objects.all()    # 查询全部数据
    count_page =10    # 按每页count_page条数据分页
    paginator = Paginator(progress_list, count_page)
    start = (int(page)-1)*count_page
    try:
        progress_data = paginator.page(page)
    # 显示第一页,传入page的值为None或空，默认为1
    except PageNotAnInteger:
        progress_data = paginator.page(1)
    # 传入page值不在有效范围
    except EmptyPage:
        progress_data = paginator.page(paginator.num_pages)
    context = {
        'progress_data': progress_data,
        'start': start,
        'search_data': search_data,
        'username': request.user,
    }
    return render(request, 'project/progress.html', context)


# 导入进度数据
def progress_import(request):
    if request.method == 'POST':
        progress_file = request.FILES.get('progress_file')
        file_type = progress_file.name.split('.')[1]  # 获取文件后缀
        if file_type in ['xlsx', 'xls']:
            date = xlrd.open_workbook(filename=None, file_contents=progress_file.read())
            tables = date.sheets()
            for table in tables:
                rows = table.nrows
                try:
                    with transaction.atomic():
                        data_table = []
                        for row in range(1, rows):
                            row_values = table.row_values(row)
                            try:
                                tasks = Task.objects.get(task_num=row_values[0])  # 判断任务是否存在
                            except Task.DoesNotExist:
                                return HttpResponse('数据中有不存在的任务！')
                            else:
                                data_table.append(Progress(
                                    tasks=tasks,
                                    date=row_values[1],
                                    executor=row_values[2],
                                    hours=row_values[3],
                                    record=row_values[4],
                                ))
                        Progress.objects.bulk_create(data_table)
                except Exception:
                    return HttpResponse('解析excel文件或者数据插入错误！')
            return HttpResponse('数据导入成功')
        else:
            return HttpResponse('上传文件类型错误！')
    return render(request, 'project/progress.html')


# 导出进度数据
def progress_download(request, model):
    sio = BytesIO()
    if model == 1:  # 模式1，导出数据
        export(Progress).save(sio)
    elif model == 2:  # 模式2，导出模板
        template(Progress).save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    response.write(sio.getvalue())
    return response


# 添加一条进度数据
def progress_add(request):
    if request.method == 'GET':
        return render(request, 'project/progress.html')

    if request.method == 'POST':
        date = request.POST.get('date')
        executor = request.POST.get('executor')
        hours = request.POST.get('hours')
        record = request.POST.get('record')
        task_num = request.POST.get('task_num')
        context = {}
        try:
            tasks = Task.objects.get(task_num=task_num)  # 判断任务是否存在
        except Task.DoesNotExist:
            context['wrong'] = '该任务不存在'
        else:
            Progress.objects.create(
                tasks=tasks,
                date=date,
                hours=hours,
                executor=executor,
                record=record,)
            return HttpResponseRedirect(reverse('project:progress'))
        return render(request, 'project/progress.html', context)


# 修改进度数据
def progress_modify(request):
    date = request.POST.get('date')
    executor = request.POST.get('executor')
    hours = request.POST.get('hours')
    record = request.POST.get('record')
    task_num = request.POST.get('task_num')
    try:
        tasks = Task.objects.get(task_num=task_num)  # 判断任务是否存在
    except Task.DoesNotExist:
        return HttpResponse('该任务不存在')
    else:
        try:
            progress = tasks.to_progress.get(date=date)  # 判断进度是否存在
        except Progress.DoesNotExist:
            return HttpResponse('任务进度不存在')
        else:
            progress.date = date
            progress.executor = executor
            progress.hours = hours
            progress.record = record
            progress.save()
        return HttpResponseRedirect(reverse('project:progress'))












