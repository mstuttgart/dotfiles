##############################################################################
#
#    Jupical Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Jupical Technologies(<http://www.jupical.com>).
#    Author: Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from odoo import http
# from odoo.http import route, request


class HTAbout(http.Controller):

    @http.route('/aboutus', auth='public', website=True)
    def about(self, **kwargs):
        return http.request.render('theme_jt_corporate2201.about_page')


class HTService(http.Controller):

    @http.route('/service', auth='public', website=True)
    def services(self, **kwargs):
        return http.request.render('theme_jt_corporate2201.service_page')


class HTPortfolio(http.Controller):

    @http.route('/portfolio', auth='public', website=True)
    def portfolio(self, **kwargs):
        return http.request.render('theme_jt_corporate2201.portfolio_page')


class HTContact(http.Controller):

    @http.route('/contactus', auth='public', website=True)
    def contact(self, **kwargs):
        return http.request.render('theme_jt_corporate2201.contact_page')
