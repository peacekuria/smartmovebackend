from app.models.inventory import Inventory


def test_inventory_item(app):
    item = Inventory(item_name="King Size Bed", quantity=1, booking_id=1)
    assert item.item_name == "King Size Bed"
    assert item.quantity == 1
