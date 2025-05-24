from odoo import fields, models, api


class RentalContract(models.Model):
    _name = 'rental.contract'
    _description = 'Contract Description'

    name = fields.Char(string="Contract Reference", required=True, copy=False, readonly=True, default='New')
    booking_id = fields.Many2one('rental.booking', string="Booking", required=True, ondelete='cascade')
    customer_id = fields.Many2one('rental.customer', string="Customer", related='booking_id.customer_id', readonly=True)
    car_id = fields.Many2one('rental.car', string="Car", related='booking_id.car_id', readonly=True)
    start_date = fields.Datetime(string="Start Date", related='booking_id.start_date', readonly=True)
    end_date = fields.Datetime(string="End Date", related='booking_id.end_date', readonly=True)
    total_price = fields.Float(string="Total Price", related='booking_id.total_price', readonly=True)
