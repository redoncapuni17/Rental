from odoo import fields, models, api


class RentalInvoiceLine(models.Model):
    _name = 'rental.invoice.line'
    _description = 'Description'

    invoice_id = fields.Many2one('rental.invoice', string='Invoice', required=True)
    booking_id = fields.Many2one('rental.booking', string='Booking', required=True)
