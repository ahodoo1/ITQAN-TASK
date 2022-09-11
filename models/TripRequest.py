from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta


class TripRequest(models.Model):
    _name = "trip.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = " Trip Request"
    _rec_name = "employee_id"
    employee_id = fields.Many2one("hr.employee", string="Employee", domain=[("contract_id.state", "=", "open")])
    destination = fields.Many2one("res.country", string="Destination")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End date", store=True)
    rest_days = fields.Integer(string="Number of Rest Days")
    trip_days = fields.Integer(string="Trip Days", compute="_set_trip_days")
    full_trip_days = fields.Integer(string="Full Trip Days", compute="_set_full_trip_days")
    status = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("ended", "Ended"), ("cancelled", "Cancelled")],
        string="Status", default="draft")
    status_change = fields.Many2one("res.users", string="Last change Status By", tracking=True,
                                    default=lambda self: self.env.user)
    company_id = fields.Many2one("res.company", string="company", default=lambda self: self.env.company)

    @api.constrains("rest_days")
    def check_rest_days(self):
        for rec in self:
            if rec.rest_days >= 0:
                if rec.rest_days >= rec.full_trip_days:
                    raise ValidationError(
                        _("""Rest days can't be equal or  greater than full trip days please \nchange the value of rest days or set it to zero"""))
            else:
                raise ValidationError(_("Rest Days cant be negative number"))

    @api.depends("end_date", "start_date")
    def _set_full_trip_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.end_date >= rec.start_date:
                    diff = rec.end_date - rec.start_date
                    rec.full_trip_days = diff.days + 1
                else:
                    rec.full_trip_days = 0
            else:
                rec.full_trip_days = 0

    @api.depends("end_date", "start_date", "rest_days")
    def _set_trip_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.end_date >= rec.start_date:
                    diff = rec.end_date - rec.start_date
                    if rec.rest_days < diff.days:
                         rec.trip_days = (diff.days + 1) - rec.rest_days
                    else:
                        rec.trip_days = 0
                else:
                    rec.trip_days = 0
            else:
                rec.trip_days = 0

    @api.onchange("start_date")
    def onchange_date_start(self):
        for record in self:
            if record.start_date:
                record.end_date = None

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        if self.start_date != False and self.end_date != False:
            if self.start_date > self.end_date:
                raise ValidationError(_(" Start Date  should not be greater than End Date."))

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        for record in self:
            if record.employee_id:
                record.destination = None
            else:
                record.destination = None

        return {'domain': {'destination': [('id', 'in', self.employee_id.allowed_destination.ids)]}}

    # @api.onchange("status")
    # def onchange_status(self):
    #     for record in self:
    #         record.status_change=self.env.user

    def update_status(self):
        ended_date = datetime.utcnow().date()
        print("cron", ended_date)
        self.env["trip.request"].search([("status", "=", "confirmed"), ("end_date", "<=", ended_date)]).write({"status": "ended"})

    def button_draft(self):
        for rec in self:
            if rec.status in ["confirmed","ended"]:
                raise ValidationError(_("you can't set to draft %s Trip ." % rec.status))
            else:
                rec.status = "draft"

    def button_confirm(self):
        for rec in self:
            if rec.status in["ended"]:
                raise ValidationError(_("you can't set to draft %s Trip ." % rec.status))
            else:
             rec.status = "confirmed"

    def button_cancel(self):
        for rec in self:
            if rec.status in ["confirmed", "ended"]:
                raise ValidationError(_("you can't cancel %s Trip ." % rec.status))
            else:
                rec.status = "cancelled"

    @api.model
    def create(self, vals):
        res = super(TripRequest, self).create(vals)
        return res

    def write(self, vals):
        if "status" in vals:
            vals["status_change"] = self.env.user
        res = super(TripRequest, self).write(vals)
        return res
