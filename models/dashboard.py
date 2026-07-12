from odoo import models, fields, api

class TransitopsDashboard(models.Model):
    _name = 'transitops.dashboard'
    _description = 'TransitOps Dashboard'

    name = fields.Char(default="Fleet Dashboard")
    active_vehicles = fields.Integer(compute='_compute_kpis')
    available_vehicles = fields.Integer(compute='_compute_kpis')
    maintenance_vehicles = fields.Integer(compute='_compute_kpis')
    active_trips = fields.Integer(compute='_compute_kpis')
    pending_trips = fields.Integer(compute='_compute_kpis')
    drivers_on_duty = fields.Integer(compute='_compute_kpis')
    fleet_utilization = fields.Float(compute='_compute_kpis')

    def _compute_kpis(self):
        for record in self:
            vehicle_model = self.env['transitops.vehicle']
            trip_model = self.env['transitops.trip']
            driver_model = self.env['transitops.driver']

            active_v = vehicle_model.search_count([('status', '=', 'on_trip')])
            avail_v = vehicle_model.search_count([('status', '=', 'available')])
            maint_v = vehicle_model.search_count([('status', '=', 'in_shop')])
            total_v = vehicle_model.search_count([('status', '!=', 'retired')])

            record.active_vehicles = active_v
            record.available_vehicles = avail_v
            record.maintenance_vehicles = maint_v
            record.active_trips = trip_model.search_count([('status', '=', 'dispatched')])
            record.pending_trips = trip_model.search_count([('status', '=', 'draft')])
            record.drivers_on_duty = driver_model.search_count([('status', 'in', ['available', 'on_trip'])])
            record.fleet_utilization = (active_v / total_v * 100.0) if total_v else 0.0
