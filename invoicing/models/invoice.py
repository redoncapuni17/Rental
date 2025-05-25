from odoo import fields, models, api


class RentalInvoice(models.Model):
    _name = 'rental.invoice'
    _description = 'Invoice Description'

    name = fields.Char(string='Invoice Number', required=True, copy=False, readonly=True, default='New')
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
            'context': {'default_invoice_id': self.id},
        }


    def action_cancelled(self):
        for invoice in self:
            invoice.status = 'cancelled'


