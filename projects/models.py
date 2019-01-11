from django.db import models
from partners.models import Partners
from bms_colowell.settings import AUTH_USER_MODEL


class ContractsInfo(models.Model):
    SHIPPING_STATUS = (
        ('1', u'已发货'),
        ('2', u'部分发货'),
        ('3', u'未发货'),
    )
    CONTRACT_TYPE = (
        ('ZS', u'正式合同'),
        ('YX', u'意向合同')
    )
    contract_id = models.CharField(
        verbose_name="合同编号", max_length=12, primary_key=True
    )
    contract_number = models.CharField(

        verbose_name="合同号", max_length=12
    )
    client = models.ForeignKey(
        Partners, verbose_name="客户", on_delete='SET_NULL', null=True, blank=True
    )
    staff_name = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="业务员", on_delete='SET_NULL', null=True,
        blank=True
    )
    box_price = models.FloatField(
        verbose_name="盒子单价", null=True, blank=True
    )
    detection_price = models.FloatField(
        verbose_name="检测单价", null=True, blank=True
    )
    contract_money = models.FloatField(
        verbose_name="合同金额", null=True, blank=True
    )
    send_date = models.DateField(
        verbose_name="寄出时间", null=True, blank=True
    )
    tracking_number = models.CharField(
        verbose_name="邮件单号", max_length=8, null=True, blank=True
    )
    send_back_date = models.DateField(
        verbose_name="寄回时间", null=True, blank=True
    )
    contract_content = models.FileField(
        verbose_name="合同内容", upload_to="#", max_length=100, null=True,
        blank=True
    )
    shipping_status = models.CharField(
        verbose_name="发货状态", max_length=1, choices=SHIPPING_STATUS,
        null=True, blank=True
    )
    contract_type = models.CharField(
        verbose_name="合同类型", max_length=3, choices=CONTRACT_TYPE,  null=True,
        blank=True
    )
    remark = models.TextField(
        verbose_name="备注", null=True, blank=True
    )
    end_status = models.BooleanField(
        verbose_name="完结状态", default=False, null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "合同信息"
        ordering = ["send_back_date"]

    def __str__(self):
        return '{}'.format(self.contract_number)


class BoxApplications(models.Model):
    CLASSIFICATION = (
        ('YY', u'已有合同'),
        ('YX', u'意向合同'),
        ('LS', u'零售'),
        ('ZS', u'赠送')
    )
    application_id = models.AutoField(
        verbose_name="编号", primary_key=True
    )
    amount = models.IntegerField(
        verbose_name="申请数量", null=True, blank=True
    )
    classification = models.CharField(
        verbose_name="申请类别", max_length=3, choices=CLASSIFICATION,
        null=True, blank=True
    )
    contract_id = models.ForeignKey(
        ContractsInfo, verbose_name="合同编号", on_delete=models.CASCADE,
        null=True, blank=True
    )
    address_name = models.CharField(
        verbose_name="收件人姓名", max_length=50, null=True, blank=True
    )
    address_phone = models.CharField(
        verbose_name="收件人号码", max_length=20, null=True, blank=True
    )
    send_address = models.CharField(
        verbose_name="邮寄地址", max_length=200, null=True, blank=True
    )
    submit_time = models.DateField(
        verbose_name="提交时间", auto_now=True
    )
    approval_status = models.BooleanField(
        verbose_name="审批状态", default=False, null=True, blank=True
    )
    box_price = models.FloatField(
        verbose_name="盒子单价", null=True, blank=True
    )
    detection_price = models.FloatField(
        verbose_name="检测单价", null=True, blank=True
    )
    use = models.CharField(
        verbose_name="用途", max_length=100, null=True, blank=True
    )
    # proposer = models.ForeignKey(
    #     AUTH_USER_MODEL, verbose_name="申请人", on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True
    # )
    proposer = models.CharField(
        verbose_name="申请人", max_length=20, null=True, blank=True
    )
    box_submit_flag = models.BooleanField(
        verbose_name="是否提交", default=False
    )

    class Meta:
        verbose_name = verbose_name_plural = "盒子申请"
        ordering = ["-submit_time"]

    def __str__(self):
        return '盒子申请编号：{}'.format(self.application_id)


class InvoiceInfo(models.Model):
    COST_TYPE_CHOICE = (
        ('BOX', u'盒子'),
        ('DET', u'检测'),
        ('ALL', u'全套'),
    )
    IVOICE_ISSUING_CHOICE = (
        ('shry', u'上海锐翌'),
        ('hzth', u'杭州拓宏'),
        ('hzry', u'杭州锐翌'),
    )
    invoice_id = models.CharField(
        verbose_name="发票编号", max_length=12, primary_key=True
    )
    contract_id = models.ForeignKey(
        ContractsInfo, verbose_name="合同号", on_delete=models.CASCADE,
        null=True, blank=True
    )
    cost_type = models.CharField(
        verbose_name="费用类型", max_length=3, choices=COST_TYPE_CHOICE,
        default="BOX"
    )
    invoice_title = models.CharField(
        verbose_name="发票抬头", max_length=100, null=True, blank=True
    )
    tariff_item = models.CharField(
        verbose_name="税号", max_length=50, null=True, blank=True
    )
    invoice_value = models.FloatField(
        verbose_name="发票金额", null=True, blank=True
    )
    tax_rate = models.FloatField(
        verbose_name="税率", null=True, blank=True
    )
    received_date = models.DateField(
        verbose_name="到账日期", null=True, blank=True
    )
    invoice_issuing = models.CharField(
        verbose_name="开票单位", choices=IVOICE_ISSUING_CHOICE,
        max_length=4, default="hzry"
    )
    receive_date = models.DateField(
        verbose_name="到账日期", null=True, blank=True
    )
    receivables = models.FloatField(
        verbose_name="应收金额", null=True, blank=True
    )
    address_name = models.CharField(
        verbose_name="收件人姓名", max_length=20, null=True, blank=True
    )
    address_phone = models.CharField(
        verbose_name="收件人号码", max_length=20, null=True, blank=True
    )
    send_address = models.CharField(
        verbose_name="寄送地址", max_length=150, null=True, blank=True
    )
    remark = models.TextField(
        verbose_name="备注", null=True, blank=True
    )
    flag = models.BooleanField(
        verbose_name="提交开票", default=False
    )
    fill_date = models.DateField(
        verbose_name="填写日期", auto_now=True
    )
    apply_name = models.CharField(
        verbose_name="申请人", max_length=20, null=True, blank=True
    )
    invoice_approval_status = models.BooleanField(
        verbose_name="审批状态", default=False, null=True, blank=True
    )

    def __str__(self):
        return "{}".format(self.invoice_id)

    class Meta:
        verbose_name = verbose_name_plural = "申请开票"
        ordering = ["fill_date"]
