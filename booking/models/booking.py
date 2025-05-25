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

    contract_ids = fields.One2many('rental.contract', 'booking_id', string='Contracts')
    contract_count = fields.Integer(string="Contracts", compute='_compute_contract_count')

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


    def action_confirm(self):
        for booking in self:
            booking.status = 'confirmed'

            contract = self.env['rental.contract'].search([
                ('booking_id', '=', booking.id),
            ], limit=1)
            if not contract:
                self.env['rental.contract'].create({
                    'booking_id': booking.id,
                    'customer_id': booking.customer_id.id,
                    'car_id': booking.car_id.id,
                    'start_date': booking.start_date,
                    'end_date': booking.end_date,
                    'total_price': booking.total_price,
                })

    def action_reset_to_draft(self):
        for booking in self:
            booking.status = 'draft'

            contract = self.env['rental.contract'].search([
                ('booking_id', '=', booking.id),
            ], limit=1)
            if contract:
                contract.unlink()

    def action_cancelled(self):
        for booking in self:
            booking.status = 'cancelled'

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids)


    def action_view_contract(self):
        self.ensure_one()
        return {
            'name': 'Contracts',
            'type': 'ir.actions.act_window',
            'res_model': 'rental.contract',
            'view_mode': 'tree,form',
            'domain': [('booking_id', '=', self.id)],
            'target': 'current',
        }
