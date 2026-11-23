from src.manager import Manager
from src.models import BlacklistedTenant, Parameters


def test_blacklist_loaded_from_file():
    """Czarna lista powinna wczytywać się z pliku jako lista obiektów modelu BlacklistedTenant."""
    manager = Manager(Parameters())
    assert isinstance(manager.blacklist, list)
    assert len(manager.blacklist) > 0
    for entry in manager.blacklist:
        assert isinstance(entry, BlacklistedTenant)
        assert isinstance(entry.name, str) and len(entry.name) > 0
        assert isinstance(entry.reason, str) and len(entry.reason) > 0


def test_is_tenant_blacklisted():
    """Metoda is_tenant_blacklisted wykrywa najemców z czarnej listy i przepuszcza pozostałych."""
    manager = Manager(Parameters())
    manager.blacklist.append(
        BlacklistedTenant(name="Marek Kowalczyk", reason="Unpaid rent for 3 months")
    )

    assert manager.is_tenant_blacklisted("Marek Kowalczyk") is True
    assert manager.is_tenant_blacklisted("Jan Nowak") is False


def test_is_tenant_blacklisted_case_insensitive():
    """Sprawdzanie czarnej listy nie powinno zależeć od wielkości liter ani spacji na końcach."""
    manager = Manager(Parameters())
    manager.blacklist.append(
        BlacklistedTenant(name="Anna Zielinska", reason="Damaged apartment equipment")
    )

    assert manager.is_tenant_blacklisted("anna zielinska") is True
    assert manager.is_tenant_blacklisted("  ANNA ZIELINSKA  ") is True