from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CharField, FloatField, BooleanField, ImageField, ForeignKey, \
    DateTimeField, SET_NULL, IntegerField, CASCADE


class Customer(Model):
    user = OneToOneField(User, null=True, blank=True, on_delete=CASCADE)
    name = CharField(max_length=200, null=True)
    email = CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=200)
    price = FloatField()
    digital = BooleanField(default=False, null=True, blank=True)
    image = ImageField(upload_to='products/', default='apps/static/store/images/placeholder.png')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(Model):
    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    date_ordered = DateTimeField(auto_now_add=True)
    complete = BooleanField(default=False)
    transaction_id = CharField(max_length=100, null=True)


    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        return sum(i.get_total for i in order_items)


    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        return sum(i.quantity for i in order_items)


    def __str__(self):
        return f'{self.id}'


class OrderItem(Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True)
    order = ForeignKey(Order, on_delete=SET_NULL, null=True)
    quantity = IntegerField(default=0, null=True, blank=True)
    date_added = DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(Model):
    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True)
    order = ForeignKey(Order, on_delete=SET_NULL, null=True)
    address = CharField(max_length=200, null=True)
    city = CharField(max_length=200, null=True)
    state = CharField(max_length=200, null=True)
    zipcode = CharField(max_length=200, null=True)
    date_added = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
