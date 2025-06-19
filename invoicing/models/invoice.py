from odoo import fields, models, api


class RentalInvoice(models.Model):
    _name = 'rental.invoice'
    _description = 'Invoice Description'
    _rec_name = 'invoice_nr'

    invoice_nr = fields.Char(string='Invoice Number', copy=False, readonly=True, default='New')
    date = fields.Date(string='Invoice Date', required=True, default=fields.Date.context_today)
    customer_id = fields.Many2one('rental.customer', string='Customer', required=True)
    invoice_line_ids = fields.One2many('rental.invoice.line', 'invoice_id', string='Invoice Lines')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    payment_method = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial Payment'),
    ], string='Payment Method', compute='_compute_payment_method', store=True)

    payment_ids = fields.One2many('rental.payment', 'invoice_id', string='Payments')

    amount_due = fields.Monetary(string='Amount Due', compute='_compute_amount_due', readonly=True)
    total_invoice_price = fields.Monetary(string="Total Invoice", compute="_compute_total_invoice_price", readonly=True, currency_field='currency_id')
    payment_lines_text = fields.Html(compute="_compute_payment_lines_text", string="Paid Details")

    @api.model
    def create(self, values):
        if values.get('invoice_nr', 'New') == 'New':
            values['invoice_nr'] = self.env['ir.sequence'].next_by_code('invoice.cp')
        res = super(RentalInvoice, self).create(values)
        return res

    def action_confirm(self):
        for invoice in self:
            invoice.status = 'posted'

    def action_reset_to_draft(self):
        for invoice in self:
            invoice.status = 'draft'


    def action_register_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Register Payment',
            'res_model': 'rental.invoice.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
                'default_customer_id': self.customer_id.id,
                'default_amount': self.amount_due,
                },
        }


    def action_cancelled(self):
        for invoice in self:
            invoice.status = 'cancelled'

    @api.depends('amount_due', 'total_invoice_price')
    def _compute_payment_method(self):
        for invoice in self:
            if invoice.amount_due == 0:
                invoice.payment_method = 'paid'
            elif invoice.amount_due >= invoice.total_invoice_price:
                invoice.payment_method = 'unpaid'
            else:
                invoice.payment_method = 'partial'

    @api.depends('payment_ids.amount', 'total_invoice_price', 'payment_ids.status', 'payment_ids')
    def _compute_amount_due(self):
        for invoice in self:
            total_paid = sum(p.amount for p in invoice.payment_ids if p.status == 'posted')
            invoice.amount_due = invoice.total_invoice_price - total_paid


    @api.depends('invoice_line_ids','invoice_line_ids.booking_id')
    def _compute_total_invoice_price(self):
        for invoice in self:
            invoice.total_invoice_price = sum(line.total_line for line in invoice.invoice_line_ids)

    @api.depends('payment_ids')
    def _compute_payment_lines_text(self):
        for rec in self:
            lines = []
            for payroll in rec.payment_ids:
                if payroll.status == 'posted':
                    line = f" <i>Paid on {payroll.payment_date.strftime('%d.%m.%Y')}   {payroll.currency_id.symbol}{payroll.amount} </i>"
                    lines.append(line)
            rec.payment_lines_text = '<br/>'.join(lines)