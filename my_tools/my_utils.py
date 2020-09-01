from datetime import datetime, date
import xlwt


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
        for i in range(len(fields)):
            field = item[fields[i]]  # 分离出单个字段值
            if isinstance(field, datetime):  # 判断是否为日期时间类型
                field = field.strftime("%Y-%m-%d %H:%M:%S")  # 格式化输出日期时间
            if isinstance(field, date):
                field = field.strftime("%Y-%m-%d")  # 格式化输出日期
            worksheet.write(row, i, field)
        row += 1
    return workbook


# 导出模板
def template(mod):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('MySheet')
    # 遍历字段
    num = 0
    for item in mod._meta.fields:
        worksheet.write(0, num, item.verbose_name)  # 获取字段verbose_name
        num += 1
    return workbook


