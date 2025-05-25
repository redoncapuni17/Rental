from odoo import fields, models, api


class RentalInvoicePaymentWizard(models.TransientModel):
    _name = 'rental.invoice.payment.wizard'
    _description = 'Invoice Payment Wizard Description'

    invoice_id = fields.Many2one('rental.invoice',string="Invoice", required=True)
    date = fields.Date(string="Payment Date", default=fields.Date.context_today, required=True)


    def action_register_payment(self):
        print('')