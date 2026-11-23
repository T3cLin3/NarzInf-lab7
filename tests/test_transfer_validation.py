import pytest

from src.manager import Manager
from src.models import Parameters, Transfer


def test_validate_transfers_within_limits():
    """Przelewy w zakresie [min_transfer_amount, max_transfer_amount] (włącznie) są poprawne."""
    manager = Manager(Parameters(), min_transfer_amount=-1000.0, max_transfer_amount=5000.0)
    manager.transfers = [
        Transfer(amount_pln=-1000.0, date='2025-01-01', settlement_year=2025, settlement_month=1, tenant='tenant-1', type='refund'),
        Transfer(amount_pln=2500.0, date='2025-01-05', settlement_year=2025, settlement_month=1, tenant='tenant-2', type='rent'),
        Transfer(amount_pln=5000.0, date='2025-01-10', settlement_year=2025, settlement_month=1, tenant='tenant-3', type='rent'),
    ]

    invalid_transfers = manager.validate_transfers()
    assert invalid_transfers == []


def test_validate_transfers_detects_out_of_range_amounts():
    """Metoda validate_transfers powinna zwrócić przelewy poniżej minimum lub powyżej maksimum."""
    manager = Manager(Parameters(), min_transfer_amount=-1000.0, max_transfer_amount=5000.0)
    too_low = Transfer(amount_pln=-1500.0, date='2025-01-02', settlement_year=2025, settlement_month=1, tenant='tenant-1', type='refund')
    valid = Transfer(amount_pln=2500.0, date='2025-01-05', settlement_year=2025, settlement_month=1, tenant='tenant-2', type='rent')
    too_high = Transfer(amount_pln=7500.0, date='2025-01-08', settlement_year=2025, settlement_month=1, tenant='tenant-3', type='rent')
    manager.transfers = [too_low, valid, too_high]

    invalid_transfers = manager.validate_transfers()
    assert len(invalid_transfers) == 2
    assert too_low in invalid_transfers
    assert too_high in invalid_transfers
    assert valid not in invalid_transfers


def test_manager_invalid_transfer_limits_raises_error():
    """Ustawienie min_transfer_amount większego niż max_transfer_amount powinno rzucić ValueError."""
    with pytest.raises(ValueError):
        Manager(Parameters(), min_transfer_amount=5000.0, max_transfer_amount=1000.0)