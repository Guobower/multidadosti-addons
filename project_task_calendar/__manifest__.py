# -*- coding: utf-8 -*-
#    Multidados Project
#    Copyright (C) 2016 MultidadosTI (http://www.multidadosti.com.br)
#    @author Aldo Soares <a.soares@itimpacta.org.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Project Task in Calendar',
    'license': 'AGPL-3',
    'author': 'MultidadosTI',
    'version': '10.0.1.0.0',
    'website': 'https://github.com/multidadosti-erp/multidadosti-addons',
    'summary': """Custom module developed for visual improvement on project
               module and integration with calendar Support by MultidadosTI""",
    'category': 'Project',
    'depends': [
        'project',
        'calendar',
    ],
    'data': [
        'views/view_multi_project.xml',
    ],
    'installable': True,
}