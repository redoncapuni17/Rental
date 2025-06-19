from odoo import fields, models, api
from odoo.exceptions import UserError


class RentalPayment(models.Model):
    _name = 'rental.payment'
    _description = 'Payment Description'
    _rec_name = 'payment_nr'

    payment_nr = fields.Char(string='Payment Number', copy=False, readonly=True, default='New')
    invoice_id = fields.Many2one('rental.invoice', string='Invoice', required=True)
    customer_id = fields.Many2one('rental.customer', related="invoice_id.customer_id", string='Customer', required=True)
    payment_date = fields.Date(string='Payment Date', required=True, default=fields.Date.context_today)
    amount = fields.Monetary(string='Payment Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    status = fields.Selection([('draft', 'Draft'), ('posted', 'Posted'), ('cancelled', 'Cancelled'), ], string='Status',
        default='draft')
    payment_method = fields.Selection([('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'),

    ], string='Payment Method', required=True, default='cash')

    @api.model
    def create(self, values):
        if values.get('payment_nr', 'New') == 'New':
            values['payment_nr'] = self.env['ir.sequence'].next_by_code('payment.cp')
        res = super(RentalPayment, self).create(values)
        return res
