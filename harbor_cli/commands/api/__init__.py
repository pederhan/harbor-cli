""""""
from __future__ import annotations

import typer

from . import artifact as artifact
from . import auditlog as auditlog
from . import config as config
from . import cve_allowlist as cve_allowlist
from . import gc as gc
from . import ldap as ldap
from . import project as project
from . import registry as registry
from . import replication as replication
from . import repository as repository
from . import scan as scan
from . import scanall as scanall
from . import scanner as scanner
from . import system as system
from . import user as user
from . import vulnerabilities as vulnerabilities

api_commands: list[typer.Typer] = [
    artifact.app,
    auditlog.app,
    config.app,
    cve_allowlist.app,
    gc.app,
    ldap.app,
    project.app,
    registry.app,
    replication.app,
    repository.app,
    scan.app,
    scanall.app,
    scanner.app,
    system.app,
    user.app,
]
