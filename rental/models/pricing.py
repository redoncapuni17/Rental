from odoo import fields, models, api


class RentalPricing(models.Model):
    _name = 'rental.pricing'
    _description = 'Pricing Description'

    car_id = fields.Many2one('rental.car', string='Car')
    duration = fields.Integer(string='Duration', required=True)
    unit = fields.Selection([
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
    ], string='Unit', required=True, default='day')
    price = fields.Float(string='Price', required=True)
