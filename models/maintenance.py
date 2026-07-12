from odoo import models, fields, api

class TransitopsMaintenance(models.Model):
    _name = 'transitops.maintenance'
    _description = 'Maintenance Log'

    name = fields.Char(string='Reference/Description', required=True)
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    maintenance_type = fields.Selection([
        ('routine', 'Routine'),
        ('repair', 'Repair'),
        ('accident', 'Accident'),
        ('other', 'Other')
    ], string='Maintenance Type', default='routine')
    maintenance_date = fields.Date(string='Date', default=fields.Date.context_today)
    cost = fields.Float(string='Cost', required=True)
    description = fields.Text(string='Details')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Closed')
    ], string='Status', default='draft', required=True)

    @api.model
    def create(self, vals):
        record = super(TransitopsMaintenance, self).create(vals)
        if record.vehicle_id and record.state != 'done':
            record.vehicle_id.status = 'in_shop'
        return record

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'done':
            for record in self:
                if record.vehicle_id and record.vehicle_id.status != 'retired':
                    record.vehicle_id.status = 'available'
        return super(TransitopsMaintenance, self).write(vals)
