################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPMemoryModuleMap

HPMemoryModuleMap maps the cpqSiMemModuleTable table to cpqSiMemModule objects

$Id: HPMemoryModuleMap.py,v 1.5 2011/01/05 00:22:16 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPMemoryModuleMap(SnmpPlugin):
    """Map HP/Compaq insight manager cpqSiMemModuleTable table to model."""

    maptype = "cpqHeResMem2Module"
    modname = "ZenPacks.community.HPMon.cpqHeResMem2Module"
    relname = "memorymodules"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cpqSiMemModuleTable',
                    '.1.3.6.1.4.1.232.2.2.4.5.1',
                    {
                        '.1': '_boardindex',
                        '.2': 'slot',
                        '.3': 'size',
                        '.4': '_slottype',
                        '.5': '_speed',
                        '.6': '_technology',
                        '.7': '_manufacturer',
                        '.10': 'serialNumber',
                        '.13': '_frequency',
                    }
        ),
        GetTableMap('cpqHeResMemModuleTable',
                    '.1.3.6.1.4.1.232.6.2.14.11.1',
                    {
                        '.4': 'status',
                    }
        ),
        GetTableMap('cpqHeResMem2ModuleTable',
                    '.1.3.6.1.4.1.232.6.2.14.13.1',
                    {
                        '.2': '_boardindex',
                        '.5': 'slot',
                        '.6': 'size',
                        '.7': '_slottype',
                        '.8': '_technology',
                        '.9': '_manufacturer',
                        '.12': 'serialNumber',
                        '.14': '_frequency',
                        '.19': 'status',
                    }
        ),
    )

    slottypes = {1: 'Slot',
                2: 'OnBoard',
                3: 'SingleWidth',
                4: 'DoubleWidth',
                5: 'SIMM',
                6: 'PCMCIA',
                7: 'COMPAQ',
                8: 'DIMM',
                9: 'SO-DIMM',
                10: 'RIMM',
                11: 'SRIMM',
                12: 'FB-DIMM',
                13: 'DIMM DDR',
                14: 'DIMM DDR2',
                15: 'DIMM DDR3',
                16: 'DIMM FBD2',
                17: 'FB-DIMM DDR2',
                18: 'FB-DIMM DDR3',
                }

    technologies = { 1: 'other',
                    2: 'FPM',
                    3: 'EDO',
                    4: 'burstEDO',
                    5: 'Synchronous',
                    6: 'RDRAM',
                    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cardtable = tabledata.get('cpqHeResMem2ModuleTable', {})
        if not cardtable:
            mmstt = tabledata.get('cpqHeResMemModuleTable', {})
            cardtable = tabledata.get('cpqSiMemModuleTable', {})
            for oid in cardtable.keys():
                cardtable[oid]['status'] = mmstt.get(oid, {}).get('status', 1)
            self.maptype = "cpqSiMemModule"
            self.modname = "ZenPacks.community.HPMon.cpqSiMemModule"
        rm = self.relMap()
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("Board%d %s%d" % (om._boardindex,
                                        self.slottypes.get(om._slottype,'Slot'),
                                        om.slot))
                om.size = getattr(om, 'size', 0) * 1024
                if om.size > 0:
                    model = []
                    if getattr(om, '_manufacturer', '') != '':
                        model.append(getattr(om, '_manufacturer', ''))
                        manuf = getattr(om, '_manufacturer', '')
                    else: manuf = 'Unknown'
                    if self.technologies.get(om._technology, '') != '':
                        model.append(self.technologies.get(om._technology, ''))
                    if 2 < int(getattr(om, '_slottype', 0)) < 19:
                        model.append(self.slottypes[int(om._slottype)])
                    model.append(convToUnits(om.size))
                    if getattr(om, '_frequency', 0) > 0:
                        model.append("%sMHz" % getattr(om, '_frequency', 0))
                    if getattr(om, '_speed', 0) > 0:
                        model.append("%sns" % getattr(om, '_speed', 0))
                    om.setProductKey = MultiArgs(" ".join(model), manuf)
                else:
                    om.monitor = False
                rm.append(om)
            except AttributeError:
                continue
        return rm

