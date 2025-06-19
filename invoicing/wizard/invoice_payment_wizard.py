from odoo import fields, models, api
from odoo.exceptions import UserError


class RentalInvoicePaymentWizard(models.TransientModel):
    _name = 'rental.invoice.payment.wizard'
    _description = 'Invoice Payment Wizard Description'

    invoice_id = fields.Many2one('rental.invoice',string="Invoice", required=True)
    customer_id = fields.Many2one('rental.customer', string="Customer", required=True)
    amount = fields.Monetary(string="Payment Amount", required=True, currency_field='currency_id')
    date = fields.Date(string="Payment Date", default=fields.Date.context_today, required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)

    def action_register_payment(self):
        self.ensure_one()

        if self.amount <= 0:
            raise UserError("Amount must be greater than zero")

        self.env['rental.payment'].create({
            'invoice_id': self.invoice_id.id,
            'customer_id': self.customer_id.id,
            'amount': self.amount,
            'payment_date': self.date,
            'currency_id': self.currency_id.id,
            'status': 'posted',  # or 'draft' if you want it pending
        })

        return {'type': 'ir.actions.act_window_close'}
