from odoo import fields, models, api


class RentalCategory(models.Model):
    _name = 'rental.category'
    _description = 'Category Description'

    name = fields.Char(string="Category Name", required=True)
