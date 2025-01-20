from django.forms import ModelForm


from .models import ManufactureTable, ProductTable, UserTable


class UserRegForm(ModelForm):
    class Meta:
        model = UserTable
        fields = ["Name", "Email", "Phone"]
class manufactureform(ModelForm):
    class Meta:
        model = ManufactureTable
        fields = ["CompanyName","CompanyAddress","Email","phone"]
class AddProductForm(ModelForm):
    class Meta:
        model = ProductTable
        fields = ["ProductName","ProductType","Expirydate","Uplaodphoto","Productprice"]
        



        
