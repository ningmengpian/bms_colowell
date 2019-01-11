from django.db import models
# Create your models here.
from tech_support.models import *


class ExtExecute(models.Model):
    """实验的提取表"""
    EXT_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
    )
    ext_number = models.CharField("提取编号", max_length=50)
    boxes = models.ForeignKey(BoxDeliveries, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    ext_method = models.ForeignKey(ExtMethod, verbose_name="实验方法",
                                   on_delete=models.SET_NULL, null=True)
    ext_times = models.IntegerField("提取次数")
    start_number = models.CharField("起始取样量(ml)", max_length=50)
    test_number = models.CharField("试管批次", max_length=50)
    hemoglobin = models.CharField("血红蛋白", max_length=50)
    cizhutiji = models.CharField("磁珠体积(ul)", max_length=50)
    ext_density = models.CharField("提取浓度(ng/ul)", max_length=50)
    elution_volume = models.CharField("洗脱体积(ul)", max_length=50)
    produce = models.CharField("产出(ng)", max_length=50)
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    ext_date = models.DateField("提取日期", null=True)
    note = models.TextField(verbose_name="实验异常备注",blank=True)
    status = models.IntegerField(choices=EXT_STATUS, verbose_name="状态")
    submit = models.NullBooleanField(
        verbose_name='实验完成，提交数据', default=None
    )
    fail = models.NullBooleanField(
        verbose_name='实验重做，记录数据', default=None
    )

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "1-提取任务管理"

    def __str__(self):
        return self.ext_number

class QualityTest(models.Model):
    """实验的质检表"""
    QUA_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
    )
    qua_number = models.CharField("质检编号", max_length=50)
    boxes = models.ForeignKey(BoxDeliveries, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    extexecute = models.ForeignKey(ExtExecute, verbose_name="提取信息",
                                   on_delete=models.SET_NULL, null=True)
    template_number = models.CharField("模板量", max_length=50)
    instrument = models.CharField("仪器", max_length=50)
    test_number = models.CharField("试管批次", max_length=50)
    loop_number = models.CharField("循环数", max_length=50)
    background_baseline = models.CharField("Background/Baseline",
                                           max_length=50)
    ct = models.CharField("CT值", max_length=50)
    amplification_curve = models.CharField("扩增曲线",
                                           max_length=50)
    threshold_line = models.CharField("阀值线", max_length=50)
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices= QUA_STATUS, verbose_name="状态")
    qua_date = models.DateField("质检日期", null=True)
    note = models.TextField(verbose_name="实验异常备注",default="",blank=True)
    submit = models.NullBooleanField(
        verbose_name='实验完成，提交数据', default=None
    )
    fail = models.NullBooleanField(
        verbose_name='实验重做，记录数据', default=None
    )

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "2-质检任务管理"

    def __str__(self):
        return self.qua_number


class BsTask(models.Model):
    """实验的BS表"""
    BS_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
    )
    bs_number = models.CharField("BS编号", max_length=50)
    boxes = models.ForeignKey(BoxDeliveries, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    quality_Test = models.ForeignKey(QualityTest, verbose_name="质检信息",
                                     on_delete=models.SET_NULL, null=True)
    test_number = models.CharField("试管批次", max_length=50)
    bs_times = models.IntegerField("BS次数")
    bis_begin = models.CharField("BIS起始量(ng)", max_length=50)
    bis_template = models.CharField("BIS模板量(ul)", max_length=50)
    bis_elution = models.CharField("bis洗脱体积(ul)", max_length=50)
    is_quality = models.BooleanField("有无质控")
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    bs_date = models.DateField("BS实验日期", null=True)
    note = models.TextField(verbose_name="实验异常备注",blank=True)
    status = models.IntegerField(choices=BS_STATUS, verbose_name="状态")
    submit = models.NullBooleanField(
        verbose_name='实验完成，提交数据', default=None
    )
    fail = models.NullBooleanField(
        verbose_name='实验重做，记录数据', default=None
    )

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "3-BS任务管理"

    def __str__(self):
        return self.bs_number


class FluorescenceQuantification(models.Model):
    """实验的荧光定量表"""
    FQ_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
        (3, '实验数据已核对'),
    )
    boxes = models.ForeignKey(BoxDeliveries, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    fq_number = models.CharField("荧光定量编号", max_length=50)
    bs_task = models.ForeignKey(BsTask, verbose_name="BS信息",
                                on_delete=models.SET_NULL, null=True)
    test_number = models.CharField("试管批次", max_length=50)
    instrument = models.CharField("仪器", max_length=50)
    loop_number = models.CharField("循环数", max_length=50)
    background = models.CharField("Background", max_length=50)
    actb_noise = models.CharField("NoiseBand/STDMultiplier",
                                  max_length=50)
    actb_ct = models.CharField("CT值", max_length=50)
    actb_amp = models.CharField("扩增曲线", max_length=50)
    sfrp2_noise = models.CharField("NoiseBand/STDMultiplier",
                                   max_length=50)
    sfrp2_ct = models.CharField("CT值", max_length=50)
    sfrp2_amp = models.CharField("扩增曲线", max_length=50)
    sdc2_noise = models.CharField("NoiseBand/STDMultiplier",
                                  max_length=50)
    sdc2_ct = models.CharField("CT值", max_length=50)
    sdc2_amp = models.CharField("扩增曲线", max_length=50)
    is_quality = models.BooleanField("有无质控")
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    fq_date = models.DateField("荧光定量日期", null=True)
    qpcr_index = models.CharField("QPCR反馈", max_length=50)
    qpcr_suggest = models.CharField("建议", max_length=200)
    status = models.IntegerField(choices=FQ_STATUS, verbose_name="状态")
    result = models.TextField("结果")
    note = models.TextField(verbose_name="实验异常备注",blank=True)
    submit = models.NullBooleanField(
        verbose_name='实验完成，提交数据', default=None
    )
    fail = models.NullBooleanField(
        verbose_name='实验重做，记录数据', default=None
    )

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "4-荧光定量管理"

    def __str__(self):
        return self.fq_number
