from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 列表页配置
    list_display = (
        'name', 
        'formatted_id_card', 
        'gender', 
        'grade_display',
        'age_display', 
        'parent_contact'
    )
    list_filter = ('grade',)
    search_fields = ('name', 'id_card', 'parent_contact')
    list_per_page = 20

    # 详情页配置
    fieldsets = (
        ('身份信息', {
            'fields': (
                'id_card', 
                'name', 
                ('birth_date', 'age_display'), 
                'gender'
            ),
            'description': '基本信息（*身份证号保存后不可修改）'
        }),
        ('学业信息', {
            'fields': ('grade',),
            'description': '当前就读信息'
        }),
        ('家庭信息', {
            'fields': (
                'address', 
                'parent_name', 
                'parent_contact'
            ),
            'description': '家庭联系信息'
        }),
    )
    readonly_fields = ('birth_date', 'gender', 'age_display')

    # 自定义显示方法
    def formatted_id_card(self, obj):
        """脱敏显示身份证号"""
        return f"{obj.id_card[:6]}********{obj.id_card[-4:]}"
    formatted_id_card.short_description = '身份证号'

    def grade_display(self, obj):
        return obj.get_grade_display()
    grade_display.short_description = '所在年级'

    def age_display(self, obj):
        return f"{obj.age} 岁"
    age_display.short_description = '年龄'

    # 数据保护
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id_card',)
        return self.readonly_fields

    # 信息提示
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['id_card'].help_text = "保存后将自动生成出生日期和性别，且不可修改"
        form.base_fields['grade'].help_text = "请选择当前实际就读年级"
        return form

    # 界面优化
    list_display_links = ('name', 'formatted_id_card')
    empty_value_display = '-空-'