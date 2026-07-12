from odoo import models, fields

class TransitopsExpense(models.Model):
    _name = 'transitops.expense'
    _description = 'Expense Record'

    name = fields.Char(string='Description', required=True)
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    expense_type = fields.Selection([
        ('fuel', 'Fuel'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other')
    ], string='Type', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    cost = fields.Float(string='Cost', required=True)
    description = fields.Text(string='Details')
