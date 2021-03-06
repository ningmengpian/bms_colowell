from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget, ForeignKeyWidget

from bs_invoices.models import Invoices, Payment, BusinessRecord
from bms_colowell.settings import AUTH_USER_MODEL
from projects.models import ContractsInfo


class InvoicesResources(resources.ModelResource):
    """发票详细信息rsources"""

    id = Field(
        column_name='编号', attribute='id', default=None
    )
    invoice_id = Field(
        column_name="发票编号", attribute='invoice_id'
    )
    salesman = Field(
        column_name="业务员", attribute='salesman',
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_number', default=None
    )
    invoice_type = Field(
        column_name="开票类型", attribute='invoice_type'
    )
    invoice_issuing = Field(
        column_name="开票单位", attribute='invoice_issuing',
        readonly=True,
    )
    invoice_title = Field(
        column_name="抬头", attribute='invoice_title'
    )
    tariff_item = Field(
        column_name="税号", attribute='tariff_item'
    )
    send_address = Field(
        column_name="对方地址", attribute='send_address'
    )
    address_phone = Field(
        column_name="号码", attribute='address_phone'
    )
    opening_bank = Field(
        column_name="开户行", attribute='opening_bank'
    )
    bank_account_number = Field(
        column_name="账号", attribute='bank_account_number'
    )
    invoice_value = Field(
        column_name="开票金额", attribute='invoice_value', default=None
    )
    invoice_content = Field(
        column_name="发票内容", attribute='invoice_content'
    )
    remark = Field(
        column_name="备注", attribute='remark'
    )
    apply_name = Field(
        column_name="申请人", attribute='apply_name__username', default=None,
    )
    receive_value = Field(
        column_name="到账金额", attribute='receive_value', default=None
    )
    receive_date = Field(
        column_name="到账时间", attribute='receive_date', default=None,
        widget=DateWidget(format='%Y-%m-%d'),
    )
    invoice_number = Field(
        column_name="发票号码", attribute='invoice_number'
    )
    billing_date = Field(
        column_name="开票日期", attribute='billing_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    invoice_send_date = Field(
        column_name="寄出日期", attribute='invoice_send_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    tracking_number = Field(
        column_name="快递单号", attribute='tracking_number'
    )
    tax_rate = Field(
        column_name="税率", attribute='tax_rate', default=None
    )
    fill_name = Field(
        column_name="填写人", attribute='fill_name', default=None
    )
    send_flag = Field(
        column_name="是否提交", attribute='send_flag'
    )
    record_number = Field(
        column_name="业务流编号", attribute='record_number',
        widget=ForeignKeyWidget(BusinessRecord, 'record_number')
    )

    class Meta:
        model = Invoices
        fields = (
            'id', 'invoice_id', 'salesman', 'contract_number', 'invoice_type',
            'invoice_issuing', 'invoice_title', 'tariff_item',
            'send_address', 'address_phone', 'opening_bank',
            'bank_account_number', 'invoice_value', 'remark',
            'invoice_content', 'apply_name', 'receive_value', 'receive_date',
            'invoice_number', 'billing_date', 'invoice_send_date',
            'tracking_number', 'tax_rate', 'fill_name', 'send_flag',
            'record_number',
        )
        export_order = fields
        skip_unchanged = True
        import_id_fields = ['id']

    def dehydrate_contract_number(self, invoices):
        contract_number = None
        if invoices.record_number is not None:
            contract_number = invoices.record_number.contract_number.contract_number
        return contract_number

    def dehydrate_invoice_issuing(self, invoices):
        issuing_entities = {'shry': '上海锐翌', 'hzth': '杭州拓宏', 'hzry': '杭州锐翌',
                            'sdry': '山东锐翌'}
        return issuing_entities[invoices.invoice_issuing]


class PaymentResource(resources.ModelResource):
    id = Field(
        column_name="编号", attribute='id', default=None
    )
    payment_number = Field(
        column_name="到账编号", attribute='payment_number', default=None
    )
    contract_number = Field(
        column_name="合同号", default=None
    )
    receive_value = Field(
        column_name="到账金额", attribute='receive_value', default=None
    )
    wait_invoices = Field(
        column_name="待开票额", attribute='wait_invoices', default=None
    )
    receive_date = Field(
        column_name="到账时间", attribute='receive_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    record_number = Field(
        column_name="业务流编号", attribute='record_number',
        widget=ForeignKeyWidget(BusinessRecord, 'record_number')
    )

    class Meta:
        model = Payment
        fields = (
            'id', 'payment_number', 'contract_number', 'receive_value',
            'wait_invoices', 'receive_date', 'record_number'
        )
        export_order = (
            'id',  'payment_number', 'contract_number', 'receive_value',
            'wait_invoices', 'receive_date',
        )
        skip_unchanged = True
        import_id_fields = ['id']

    def dehydrate_contract_number(self, payment):
        contract_number = payment.record_number.contract_number.contract_number
        return contract_number

    def get_export_headers(self):
        export_headers = [
            "编号", "到款编号", "合同号", "到账金额", "待开票额", "到账时间", '业务流编号'
        ]
        return export_headers
