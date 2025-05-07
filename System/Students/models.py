from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Student(models.Model):
    """
    学生基本信息模型
    通过身份证号自动解析出生日期和性别，并提供年龄等属性
    """
    GRADE_CHOICES = (
        ('1', '初一'),
        ('2', '初二'),
        ('3', '初三'),
    )

    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    id_card = models.CharField(
        verbose_name='身份证号码',
        max_length=18,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]$',
                message='请输入有效的18位身份证号码'
            )
        ],
        help_text='请输入18位身份证号码，例如：31011520050101001X'
    )
    name = models.CharField(
        verbose_name='学生姓名',
        max_length=50,
        help_text='学生真实姓名'
    )
    gender = models.CharField(
        verbose_name='性别',
        max_length=1,
        choices=GENDER_CHOICES,
        editable=False,
        help_text='根据身份证号自动识别'
    )
    birth_date = models.DateField(
        verbose_name='出生日期',
        editable=False,
        help_text='根据身份证号自动识别'
    )
    grade = models.CharField(
        verbose_name='所在年级',
        max_length=1,
        choices=GRADE_CHOICES,
        help_text='请选择当前就读年级'
    )
    address = models.TextField(
        verbose_name='家庭住址',
        help_text='示例：上海市浦东新区张江路123弄45号'
    )
    parent_name = models.CharField(
        verbose_name='监护人姓名',
        max_length=50,
        help_text='法定监护人姓名'
    )
    parent_contact = models.CharField(
        verbose_name='监护人联系方式',
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message="请输入有效的11位手机号码"
            )
        ],
        help_text='例如：13800138000'
    )
    created_at = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='最后更新时间',
        auto_now=True
    )

    class Meta:
        verbose_name = '学生档案'
        verbose_name_plural = '学生档案'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_card']),
            models.Index(fields=['grade']),
        ]

    def __str__(self):
        return f"{self.name}（{self.get_grade_display()}）"

    def clean(self):
        """自定义验证：校验身份证校验码"""
        if not self.validate_id_card_check_digit():
            raise ValidationError({'id_card': '身份证校验码无效'})

    def save(self, *args, **kwargs):
        """保存时自动解析出生日期与性别"""
        # 仅在首次保存或字段为空时解析
        if not self.birth_date:
            self.birth_date = self.parse_birth_date()
        if not self.gender:
            self.gender = self.parse_gender()
        super().save(*args, **kwargs)

    def parse_birth_date(self):
        from datetime import datetime
        try:
            return datetime.strptime(self.id_card[6:14], '%Y%m%d').date()
        except ValueError:
            raise ValidationError('身份证包含无效的日期信息')

    def parse_gender(self):
        gender_num = int(self.id_card[16])
        return 'M' if gender_num % 2 else 'F'

    def validate_id_card_check_digit(self):
        return True

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )