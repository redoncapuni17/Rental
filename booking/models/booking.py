from odoo import fields, models, api


class RentalBooking(models.Model):
    _name = 'rental.booking'
    _description = 'Booking Description'
    _rec_name = 'name'

    name = fields.Char(string="Booking", required=True, copy=False, readonly=True, default='New')
    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required=True)
    rent_price = fields.Float('Rent Price', related='car_id.rent_price', readonly=True)

    duration = fields.Integer('Duration(day)', compute='_compute_duration')
    total_price = fields.Float('Total Price', compute='_compute_total_price')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')


    # Many2one relationship
    customer_id = fields.Many2one('rental.customer', string="Customer", required=True)
    car_id = fields.Many2one('rental.car', string="Car", required=True )

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', 'New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code('rental.booking.seq') or 'New'
        result = super(RentalBooking, self).create(vals_list)
        return result


    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for booking in self:
            if booking.start_date and booking.end_date:
                start = fields.Datetime.from_string(booking.start_date)
                end = fields.Datetime.from_string(booking.end_date)
                duration = (end - start).days
                booking.duration = duration
            else:
                booking.duration = 0

    @api.depends('duration', 'rent_price')
    def _compute_total_price(self):
        for booking in self:
            if booking.duration and booking.rent_price:
                booking.total_price = booking.duration * booking.rent_price
            else:
                booking.total_price = 0.0
