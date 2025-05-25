from odoo import fields, models, api


class RentalInvoiceLine(models.Model):
    _name = 'rental.invoice.line'
    _description = 'Description'

    invoice_id = fields.Many2one('rental.invoice', string='Invoice', required=True)
    customer_id = fields.Many2one('rental.customer', related="invoice_id.customer_id", string='Customer', required=True)
    booking_id = fields.Many2one('rental.booking', string='Booking', required=True,
                                 domain="[('customer_id', '=', customer_id)]")

    car_id = fields.Many2one('rental.car', related="booking_id.car_id", string='Car', required=True)
    duration = fields.Integer(string='Duration', related="booking_id.duration", required=True, help='Duration in days')
    total_price = fields.Float(string='Total Price', related="booking_id.total_price", required=True, help='Total price for the booking')
