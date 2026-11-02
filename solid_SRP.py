# Class for baking bread
class BreadBaker:
    def bakeBread(self):
        print("Baking high-quality bread...")

# Class for managing inventory
class InventoryManager:
    def manageInventory(self):
        print("Managing inventory...")

# Class for ordering supplies
class SupplyOrder:
    def orderSupplies(self):
        print("Ordering supplies...")

# Class for serving customers
class CustomerService:
    def serveCustomer(self):
        print("Serving customers...")

# Class for cleaning the bakery
class BakeryCleaner:
    def cleanBakery(self):
        print("Cleaning the bakery...")

def main():
    baker = BreadBaker()
    inventoryManager = InventoryManager()
    supplyOrder = SupplyOrder()
    customerService = CustomerService()
    cleaner = BakeryCleaner()

    # Each class focuses on its specific responsibility
    baker.bakeBread()
    inventoryManager.manageInventory()
    supplyOrder.orderSupplies()
    customerService.serveCustomer()
    cleaner.cleanBakery()

if __name__ == "__main__":
    main()