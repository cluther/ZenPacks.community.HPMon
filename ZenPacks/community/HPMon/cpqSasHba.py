################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSasHba

cpqSasHba is an abstraction of a HP SAS Host Bus Adapter.

$Id: cpqSasHba.py,v 1.2 2011/01/04 23:24:34 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from HPExpansionCard import HPExpansionCard
from HPComponent import *

class cpqSasHba(HPExpansionCard):
    """SAS HBA object"""

    FWRev = ""

    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'cpqSasHba',
            'meta_type'      : 'cpqSasHba',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqSasHba',
            'immediate_view' : 'viewCpqSasHba',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqSasHba'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

InitializeClass(cpqSasHba)
