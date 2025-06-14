from email.policy import default

from odoo import fields, models, api


class RentalCar(models.Model):
    _name = 'rental.car'
    _description = 'Car Description'

    name = fields.Char('Name', required=True)
    license_plate = fields.Char('License Plate', required=True)
    model = fields.Char('Model', required=True)
    year = fields.Integer('Year', required=True)
    fuel_type = fields.Selection([
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], string='Fuel Type', required=True, default='diesel')
    transmission = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ], string='Transmission', required=True, default='manual')
    seat_count = fields.Integer('Seat Count', required=True)
    rent_price = fields.Float('Rent Price', required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'In Maintenance'),
    ], default='available', string="Car Status")
    image = fields.Image('Car Image')

    # Many2one relationship
    tag_ids = fields.Many2many('rental.tags', string='Tags')


