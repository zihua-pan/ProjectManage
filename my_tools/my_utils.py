from datetime import datetime
import xlrd
import xlwt
from django.db import transaction

# 导出数据
def export(mod):
    mod_set = mod.objects.values()

    # 创建excel表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('MySheet')

    # 遍历字段
    fields = []
    num = 0
    for item in mod._meta.fields:
        worksheet.write(0, num, item.verbose_name)  # 获取字段verbose_name
        fields.append(item.attname)  # 获取字段名
        num += 1

    # 遍历数据写入表
    row = 1
    for item in mod_set:
        for i in range(0, len(fields)):
            field = item[fields[i]]  # 分离出单个字段值
            if isinstance(field, datetime):  # 判断是否为日期时间类型
                field = field.strftime("%Y-%m-%d %H:%M:%S")  # 格式化输出日期时间
            worksheet.write(row, i, field)
        row += 1
    return workbook

 # 导入数据
def import_data(file, mod):
        file_type = file.name.split('.')[1]  # 获取文件格式
        if file_type in ['xlsx', 'xls']:  # 判断文件格式
            data = xlrd.open_workbook(filename=None, file_contents=file.read())
            tables = data.sheets()  # 创建页签
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
                    return HttpResponse('解析excel文件或者数据插入错误！')
            return HttpResponse('数据导入成功')
        else:
            return HttpResponse('上传文件类型错误！')
    return render(request, 'project/product.html', context)

