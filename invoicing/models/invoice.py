from odoo import fields, models, api


class RentalInvoice(models.Model):
    _name = 'rental.invoice'
    _description = 'Invoice Description'

    name = fields.Char(string='Invoice Number', required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string='Invoice Date', required=True, default=fields.Date.context_today)
    customer_id = fields.Many2one('rental.customer', string='Customer', required=True)
    invoice_line_ids = fields.One2many('rental.invoice.line', 'invoice_id', string='Invoice Lines')
    car_id = fields.Many2one('rental.car', string='Car', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('unpaid', 'Unpaid')
    ], string='Status', default='draft')



