from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TransitopsTrip(models.Model):
    _name = 'transitops.trip'
    _description = 'Transit Trip'

    source = fields.Char(string='Source', required=True)
    destination = fields.Char(string='Destination', required=True)
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('transitops.driver', string='Driver', required=True)
    cargo_weight = fields.Float(string='Cargo Weight')
    planned_distance = fields.Float(string='Planned Distance')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True)

    @api.constrains('cargo_weight', 'vehicle_id')
    def _check_cargo_weight(self):
        for record in self:
            if record.vehicle_id and record.cargo_weight > record.vehicle_id.max_load_capacity:
                raise ValidationError("Cargo weight cannot exceed the vehicle's maximum load capacity.")

    @api.constrains('vehicle_id', 'status')
    def _check_vehicle_status(self):
        for record in self:
            if record.vehicle_id:
                if record.vehicle_id.status in ('in_shop', 'retired'):
                    raise ValidationError("Cannot select a vehicle that is 'In Shop' or 'Retired'.")
                if record.status == 'draft' and record.vehicle_id.status == 'on_trip':
                    raise ValidationError("Cannot select a vehicle that is currently 'On Trip'.")

    @api.constrains('driver_id', 'status')
    def _check_driver_status(self):
        for record in self:
            if record.driver_id:
                if record.driver_id.status == 'suspended':
                    raise ValidationError("Cannot select a driver that is 'Suspended'.")
                if record.driver_id.license_expiry_date and record.driver_id.license_expiry_date < fields.Date.today():
                    raise ValidationError("Cannot select a driver whose license has expired.")
                if record.status == 'draft' and record.driver_id.status == 'on_trip':
                    raise ValidationError("Cannot select a driver that is currently 'On Trip'.")

    @api.model
    def create(self, vals):
        res = super(TransitopsTrip, self).create(vals)
        if res.status == 'dispatched':
            if res.vehicle_id:
                res.vehicle_id.status = 'on_trip'
            if res.driver_id:
                res.driver_id.status = 'on_trip'
        return res

    def write(self, vals):
        if 'status' in vals or 'vehicle_id' in vals or 'driver_id' in vals:
            for record in self:
                old_status = record.status
                old_vehicle = record.vehicle_id
                old_driver = record.driver_id
                
                super(TransitopsTrip, record).write(vals)
                
                new_status = record.status
                new_vehicle = record.vehicle_id
                new_driver = record.driver_id
                
                if old_status != new_status or old_vehicle != new_vehicle or old_driver != new_driver:
                    if old_status == 'dispatched' and new_status in ('completed', 'cancelled'):
                        if old_vehicle:
                            old_vehicle.status = 'available'
                        if old_driver:
                            old_driver.status = 'available'
                    if new_status == 'dispatched':
                        if new_vehicle:
                            new_vehicle.status = 'on_trip'
                        if new_driver:
                            new_driver.status = 'on_trip'
                        if old_vehicle and old_vehicle != new_vehicle:
                            old_vehicle.status = 'available'
                        if old_driver and old_driver != new_driver:
                            old_driver.status = 'available'
            return True
        return super(TransitopsTrip, self).write(vals)
