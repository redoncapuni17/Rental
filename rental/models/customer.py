from odoo import fields, models, api


class RentalCustomer(models.Model):
    _name = 'rental.customer'
    _description = 'Customer Description'

    name = fields.Char('Full Name', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    address = fields.Text('Address')
    driver_license = fields.Char('Driver License Number')
    image = fields.Image(string='Image')