# Copyright (C) 2007  Matthew Neeley
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from labrad import constants as C
from labrad.interfaces import ILabradProtocol, ILabradManager
from labrad.util import mangle

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python.components import registerAdapter

from zope.interface import Interface, implements

class ClientManager:
    """Adapt client to the ILabradManager interface."""
    
    implements(ILabradManager)
    
    def __init__(self, cxn):
        self.cxn = cxn

    def _send(self, packet, *args, **kw):
        """Send a request to the manager."""
        return self.cxn.sendRequest(C.MANAGER_ID, packet, *args, **kw)

    @inlineCallbacks
    def _getIDList(self, setting, data=None):
        resp = yield self._send([(setting, data)])
        names = self._mangleIDList(resp[0][1])
        returnValue(names)

    def _mangleIDList(self, L):
        return [(mangle(name), name, ID) for ID, name in L]
        
    def getServersList(self):
        """Get a list of connected servers."""
        return self._getIDList(C.SERVERS_LIST)

    @inlineCallbacks
    def getServerInfo(self, serverID):
        """Get information about a server."""
        packet = [(C.HELP, long(serverID)),
                  (C.SETTINGS_LIST, long(serverID))]
        resp = yield self._send(packet)
        descr, notes = resp[0][1]
        settings = self._mangleIDList(resp[1][1])
        returnValue((descr, notes, settings))

    def getSettingsList(self, serverID):
        """Get a list of settings for a server."""
        return self._getIDList(C.SETTINGS_LIST, serverID)

    @inlineCallbacks
    def getSettingInfo(self, serverID, settingID):
        """Get information about a setting."""
        packet = [(C.HELP, (long(serverID), long(settingID)))]
        resp = yield self._send(packet)
        description, accepts, returns, notes = resp[0][1]
        returnValue((description, accepts, returns, notes))

registerAdapter(ClientManager, ILabradProtocol, ILabradManager)