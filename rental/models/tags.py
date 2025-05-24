from odoo import fields, models, api


class RentalTags(models.Model):
    _name = 'rental.tags'
    _description = 'Tags Description'

    name = fields.Char(string="Tags Name", required=True)
    description = fields.Text(string="Tags Description")
    color = fields.Integer(string="Color", default=0)
    sequence = fields.Integer(string="Sequence", default=10)
