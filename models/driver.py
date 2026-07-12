from odoo import models, fields

class TransitopsDriver(models.Model):
    _name = 'transitops.driver'
    _description = 'Transit Driver'

    name = fields.Char(string='Name', required=True)
    license_number = fields.Char(string='License Number', required=True)
    license_category = fields.Char(string='License Category')
    license_expiry_date = fields.Date(string='License Expiry Date')
    contact_number = fields.Char(string='Contact Number')
    safety_score = fields.Float(string='Safety Score')
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended')
    ], string='Status', default='available', required=True)
