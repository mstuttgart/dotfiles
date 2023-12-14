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
    "name": "Corporate Multi Page Theme",
    "summary": "Corporate multi page with mega-menus responsive theme",
    'description': 'Corporate multi page with mega-menus responsive theme',
    'version': '12.0.0.1',
    'category': 'Theme/Corporate',
    'author': 'Jupical Technologies Pvt. Ltd.',
    'maintainer': 'Jupical Technologies Pvt. Ltd.',
    'website': 'https://www.jupical.com',
    "depends": [
        'web',
        'portal',
        'website',
        'website_blog',
        'website_crm',
        'mass_mailing',
        'website_hr_recruitment',
        'website_event',
    ],
    'data': [
        'data/        'data/theme_default_data.xml',
'
        'views/assets.xml',
        'views/layout.xml',
        'views/homepage.xml',
        'views/about_page.xml',
        'views/services_page.xml',
        'views/portfolio_page.xml',
        'views/contact_page.xml',
        'views/signup_page.xml',
        'views/events_page.xml',
        'views/blog_page.xml',
        'views/career_page.xml',
        'views/snippets.xml',
    ],
    "license": "OPL-1",
    'application': True,
    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/banner.gif',
        'static/description/theme_screenshot.png',
    ],
    'price': 50.00,
    'currency': 'EUR',
}
