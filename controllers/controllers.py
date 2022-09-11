# -*- coding: utf-8 -*-
# from odoo import http


# class TripRequest(http.Controller):
#     @http.route('/trip__request/trip__request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trip__request/trip__request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('trip__request.listing', {
#             'root': '/trip__request/trip__request',
#             'objects': http.request.env['trip__request.trip__request'].search([]),
#         })

#     @http.route('/trip__request/trip__request/objects/<model("trip__request.trip__request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trip__request.object', {
#             'object': obj
#         })
