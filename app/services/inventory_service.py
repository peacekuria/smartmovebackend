class InventoryService:
    @staticmethod
    def get_item(item_id):
        """
        Retrieves an inventory item by its ID.
        """
        print(f"Retrieving inventory item with ID: {item_id}")
        # Placeholder for actual database query
        return {"id": item_id, "name": f"Item {item_id}", "quantity": 10}

    @staticmethod
    def add_item(item_data):
        """
        Adds a new item to the inventory.
        """
        print(f"Adding new inventory item: {item_data}")
        # Placeholder for actual database insertion
        return {"id": 1, **item_data} # Simulate item creation

    @staticmethod
    def update_item_quantity(item_id, quantity_change):
        """
        Updates the quantity of an existing inventory item.
        """
        print(f"Updating quantity for item {item_id} by {quantity_change}")
        # Placeholder for actual database update
        return {"id": item_id, "name": f"Item {item_id}", "quantity": 10 + quantity_change}

    @staticmethod
    def delete_item(item_id):
        """
        Deletes an inventory item.
        """
        print(f"Deleting inventory item with ID: {item_id}")
        # Placeholder for actual database deletion
        return {"message": f"Item {item_id} deleted successfully"}
