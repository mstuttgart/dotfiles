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
{
    'name': 'Corporate Multi Page Theme',
    'summary': 'Corporate multi page with mega-menus responsive theme',
    'description': 'Corporate multi page with mega-menus responsive theme',
    'version': '12.0.0.1',
    'category': 'Theme/Corporate',
    'author': 'Jupical Technologies Pvt. Ltd.',
    'maintainer': 'Jupical Technologies Pvt. Ltd.',
    'website': 'https://www.jupical.com',
    'depends': [
        'website',
        'website_blog',
        'website_crm',
        'mass_mailing',
        'website_hr_recruitment',
        'website_event',
    ],
    'data': [
        'template/assets.xml',
        'template/layout.xml',
        'template/homepage.xml',
        'template/about_page.xml',
        'template/services_page.xml',
        'template/portfolio_page.xml',
        'template/contact_page.xml',
        'template/signup_page.xml',
        'template/events_page.xml',
        'template/blog_page.xml',
        'template/career_page.xml',
        'template/snippets.xml',
    ],
    'license': 'OPL-1',
    'application': False,
    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/banner.gif',
        'static/description/theme_screenshot.png',
    ],
    'price': 50.00,
    'currency': 'EUR',
}
