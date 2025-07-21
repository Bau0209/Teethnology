from app import db

class InventoryCategory(db.Model):
    __tablename__ = 'inventory_category'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    item_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('inventory_category.category_id'), nullable=False)
    
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quantity_unit = db.Column(db.String(50), nullable=False)
    storage_location = db.Column(db.String(255))
    cost_per_unit = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    supplier_name = db.Column(db.String(255))
    description = db.Column(db.Text)

    branch = db.relationship('Branch', backref='inventory_items', lazy=True)
    category = db.relationship('InventoryCategory', backref='items', lazy=True)

class InventoryConsumable(db.Model):
    __tablename__ = 'inventory_consumables'

    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.item_id'), primary_key=True)
    expiration_date = db.Column(db.Date)
    last_restock = db.Column(db.Date)
    minimum_stock = db.Column(db.Float)
    stock_status = db.Column(db.Enum('in stock', 'low stock', 'out of stock'), default='in stock')

    item = db.relationship('InventoryItem', backref=db.backref('consumable_info', uselist=False), lazy=True)

class InventoryEquipment(db.Model):
    __tablename__ = 'inventory_equipments'

    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.item_id'), primary_key=True)
    last_maintenance = db.Column(db.Date)
    model = db.Column(db.String(100))
    warranty_info = db.Column(db.String(255))
    date_acquired = db.Column(db.Date)
    equipment_condition = db.Column(db.String(100))

    item = db.relationship('InventoryItem', backref=db.backref('equipment_info', uselist=False), lazy=True)

class InventorySterilization(db.Model):
    __tablename__ = 'inventory_sterilization'

    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.item_id'), primary_key=True)
    expiration_date = db.Column(db.Date)
    last_restock = db.Column(db.Date)
    minimum_stock_level = db.Column(db.Float)
    size = db.Column(db.String(100))
    stock_status = db.Column(db.Enum('in stock', 'low stock', 'out of stock'), default='in stock')

    item = db.relationship('InventoryItem', backref=db.backref('sterilization_info', uselist=False), lazy=True)

class InventoryLabMaterial(db.Model):
    __tablename__ = 'inventory_lab_materials'

    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.item_id'), primary_key=True)
    expiration_date = db.Column(db.Date)
    last_restock = db.Column(db.Date)
    stock_status = db.Column(db.Enum('in stock', 'low stock', 'out of stock'), default='in stock')

    item = db.relationship('InventoryItem', backref=db.backref('lab_material_info', uselist=False), lazy=True)

class InventoryMedication(db.Model):
    __tablename__ = 'inventory_medications'

    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.item_id'), primary_key=True)
    dosage_form = db.Column(db.String(100))
    expiration_date = db.Column(db.Date)
    last_restock = db.Column(db.Date)
    strength = db.Column(db.String(100))
    batch_number = db.Column(db.String(100))
    stock_status = db.Column(db.Enum('in stock', 'low stock', 'out of stock'), default='in stock')

    item = db.relationship('InventoryItem', backref=db.backref('medication_info', uselist=False), lazy=True)
