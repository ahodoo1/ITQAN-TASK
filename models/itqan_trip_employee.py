from odoo import api, fields, _, models


class EmployeeTrip(models.Model):
    _inherit = "hr.employee"

    TripRequests_ids= fields.One2many("trip.request", "employee_id", string="Trip Requests")
    allowed_destination = fields.Many2many("res.country", string="Allowed Destinations", store=True)
    trip_count = fields.Integer("Trip count", compute="_get_trips")

    def trip_count_action(self):
        return {
            'type': "ir.actions.act_window",
            'name': "Trip Requests",
            'res_model': "trip.request",
            'view_mode': "tree,form",
            'domain': [("employee_id", "=", self.id)],
            'context': {"default_employee_id": self.id},
            'target': "current"
        }

    @api.depends("TripRequests_ids")
    def _get_trips(self):
        for rec in self:
            rec.trip_count = len(rec.TripRequests_ids)
