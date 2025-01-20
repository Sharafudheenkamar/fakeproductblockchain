from django.db import models
import hashlib
import json
from datetime import datetime


# Create your models here.
class LoginTable(models.Model):
    UserName = models.CharField(max_length=100, null=True, blank=True)
    PassWord = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

class UserTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    Phone =models.IntegerField(null=True, blank=True)

    

class ManufactureTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    CompanyName = models.CharField(max_length=100, null=True, blank=True)
    CompanyAddress = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    phone =  models.IntegerField(null=True, blank=True)

import hashlib
import json
from datetime import datetime
from django.db import models
from django.utils.timezone import now


class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(default=now)
    data = models.TextField()  # Store block data as JSON or text
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64, blank=True)

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def save(self, *args, **kwargs):
        # Automatically calculate the hash before saving
        if not self.hash:
            self.hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Block {self.index}: {self.hash}"


class Blockchain:
    @staticmethod
    def create_genesis_block():
        if not Block.objects.exists():  # Create only if no blocks exist
            Block.objects.create(
                index=0,
                timestamp=now(),
                data=json.dumps({"message": "Genesis Block"}),
                previous_hash="0",
            )

    @staticmethod
    def get_latest_block():
        return Block.objects.latest("index")

    @staticmethod
    def add_block(data):
        Blockchain.create_genesis_block()
        previous_block = Blockchain.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=now(),
            data=json.dumps(data),  # Convert Python dict to JSON string
            previous_hash=previous_block.hash,
        )
        new_block.hash = new_block.calculate_hash()
        new_block.save()

    @staticmethod
    def is_chain_valid():
        blocks = Block.objects.order_by("index")
        for i in range(1, len(blocks)):
            current_block = blocks[i]
            previous_block = blocks[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    @staticmethod
    def recalculate_hashes_after_deletion(indices_to_delete):
        # Ensure that after deletion, we need to update subsequent blocks
        for index in indices_to_delete:
            # Fetch the subsequent blocks, ordered by their index
            blocks = Block.objects.filter(index__gt=index).order_by("index")
            
            # Get the hash of the previous block
            previous_hash = Block.objects.get(index=index - 1).hash if index > 0 else "0"
            
            for block in blocks:
                # Update index, previous_hash, and hash for each subsequent block
                block.index -= 1  # Shift index by 1 to fill the gap
                block.previous_hash = previous_hash
                block.hash = block.calculate_hash()
                block.save()
                previous_hash = block.hash  

from django.db.models.signals import post_delete
from django.dispatch import receiver
import qrcode
from io import BytesIO
from django.core.files import File
class ProductTable(models.Model):
    ProductName = models.CharField(max_length=100, null=True, blank=True)
    ProductId = models.CharField(max_length=100, null=True, blank=True)
    ProductType = models.CharField(max_length=100, null=True, blank=True)
    Manufacturedate = models.DateField(null=True, blank=True)
    Expirydate = models.CharField(max_length=100, null=True, blank=True)
    Uplaodphoto = models.FileField(max_length=250, null=True, blank=True, upload_to="Media")
    Productprice = models.IntegerField(null=True, blank=True)
    QRCodeImage = models.ImageField(upload_to='product_qr_codes/', null=True, blank=True)  # To store the QR code image

    


    def __str__(self):
        return self.ProductName or "Unnamed Product"
    def save(self, *args, **kwargs):
        # Generate a QR code for the product if it's new
        if not self.QRCodeImage and self.ProductId:
            qr_code = qrcode.make(self.ProductId)  # Create QR code from ProductId
            qr_code_image = BytesIO()
            qr_code.save(qr_code_image, 'PNG')  # Save it in PNG format
            qr_code_image.seek(0)
            self.QRCodeImage = File(qr_code_image, name=f"product_{self.ProductId}_qr.png")  # Assign the QR code image to the field
        
        super(ProductTable, self).save(*args, **kwargs)  # Save the product
@receiver(post_delete, sender=ProductTable)
def delete_associated_blocks(sender, instance, **kwargs):
    # When a product is deleted, delete any associated blocks
    product_id = instance.ProductId  # Get the product ID

    # Find blocks that reference the deleted product's ID
    blocks_to_delete = Block.objects.filter(data__contains=product_id)

    # Store the blocks' indices before deleting them for recalculating hashes
    indices_to_delete = [block.index for block in blocks_to_delete]

    # Delete blocks associated with the product
    blocks_to_delete.delete()

    # Recalculate hashes for the subsequent blocks
    Blockchain.recalculate_hashes_after_deletion(indices_to_delete)
     
class FeedBack(models.Model):
    USERID=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    FeedBack = models.CharField(max_length=250, null=True, blank=True)
    Rating = models.CharField(max_length=250, null=True, blank=True)