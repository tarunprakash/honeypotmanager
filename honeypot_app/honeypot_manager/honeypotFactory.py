"""
Create/manage FTP honeypot modules
"""
import os
import sys
## required to import local opencanary files
TWISTED_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(TWISTED_DIR)

from twisted.application import service

from opencanary.config import config
from opencanary.logger import getLogger

from opencanary.modules.ftp import CanaryFTP
from opencanary.modules.ssh import CanarySSH
from opencanary.modules.http import CanaryHTTP
from opencanary.modules.mysql import CanaryMySQL

import traceback
import ipManager

class HoneypotFactory:
    honeypotClasses = {
        'FTP': CanaryFTP,
        'SSH': CanarySSH,
        'HTTP': CanaryHTTP,
        'MySQL': CanaryMySQL
    }

    def __init__(self, application):
        self.honeypots = []

        self.logger = getLogger(config)
        self.application = application
        self.config = config

    def logMsg(self, msg):
        data = {}
        data['logdata'] = {'msg': msg}
        self.logger.log(data, retry=False)

    def addHoneypot(self, klass, host):
        if type(klass) == str: ## convert honeypot class from str to class
            klass = self.honeypotClasses[klass]

        try:
            ipManager.addIp(host)
            
            obj = klass(host, self.config, self.logger)
            service = obj.getService()
            if not isinstance(service, list):
                service = [service]
            for s in service:
                s.setServiceParent(self.application)
            msg = 'Added service from class %s in %s to fake (Host: %s)' % (
                klass.__name__,
                klass.__module__,
                host
            )
            # self.logMsg({'logdata': msg})


        except Exception as e:
            err = 'Failed to add service from class %s in %s. %s' % (
                klass.__name__,
                klass.__module__,
                traceback.format_exc()
            )
            self.logMsg({'logdata': err})

        return

