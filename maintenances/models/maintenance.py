from odoo import fields, models, api


class RentalMaintenance(models.Model):
    _name = 'rental.maintenance'
    _description = 'Maintenance Description'

    name = fields.Char(string='Maintenance Reference', required=True)
    car_id = fields.Many2one('rental.car', string='Car', required=True)
    maintenance_date = fields.Date(string='Maintenance Date', required=True, default=fields.Date.context_today)
    description = fields.Text(string='Description')
    cost = fields.Float(string='Cost')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string='Status')
