from odoo import models, fields, api

class TransitopsVehicle(models.Model):
    _name = 'transitops.vehicle'
    _description = 'Transit Vehicle'

    name = fields.Char(string='Vehicle Name/Model', required=True)
    registration_number = fields.Char(string='Registration Number', required=True)
    vehicle_type = fields.Selection([
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('sedan', 'Sedan'),
        ('other', 'Other')
    ], string='Type', required=True)
    max_load_capacity = fields.Float(string='Maximum Load Capacity')
    odometer = fields.Float(string='Odometer')
    acquisition_cost = fields.Float(string='Acquisition Cost')
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired')
    ], string='Status', default='available', required=True)

    maintenance_ids = fields.One2many('transitops.maintenance', 'vehicle_id')
    expense_ids = fields.One2many('transitops.expense', 'vehicle_id')
    trip_ids = fields.One2many('transitops.trip', 'vehicle_id')

    total_operational_cost = fields.Float(string='Total Operational Cost', compute='_compute_total_operational_cost', store=True)
    revenue = fields.Float(string='Revenue')
    roi = fields.Float(string='Vehicle ROI', compute='_compute_roi', store=True)

    _sql_constraints = [
        ('registration_number_unique', 'unique(registration_number)', 'The vehicle registration number must be unique!')
    ]

    @api.depends('maintenance_ids.cost', 'expense_ids.cost', 'expense_ids.expense_type')
    def _compute_total_operational_cost(self):
        for vehicle in self:
            fuel_expenses = sum(vehicle.expense_ids.filtered(lambda e: e.expense_type == 'fuel').mapped('cost'))
            maintenance_expenses = sum(vehicle.maintenance_ids.mapped('cost')) + sum(vehicle.expense_ids.filtered(lambda e: e.expense_type == 'maintenance').mapped('cost'))
            vehicle.total_operational_cost = fuel_expenses + maintenance_expenses

    @api.depends('revenue', 'maintenance_ids.cost', 'expense_ids.cost', 'expense_ids.expense_type', 'acquisition_cost')
    def _compute_roi(self):
        for vehicle in self:
            fuel_expenses = sum(vehicle.expense_ids.filtered(lambda e: e.expense_type == 'fuel').mapped('cost'))
            maintenance_expenses = sum(vehicle.maintenance_ids.mapped('cost')) + sum(vehicle.expense_ids.filtered(lambda e: e.expense_type == 'maintenance').mapped('cost'))
            if vehicle.acquisition_cost:
                vehicle.roi = (vehicle.revenue - (maintenance_expenses + fuel_expenses)) / vehicle.acquisition_cost
            else:
                vehicle.roi = 0.0
