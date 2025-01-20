from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from .models import Block, FeedBack, LoginTable, ManufactureTable, ProductTable
from sampleApp.form import  AddProductForm, UserRegForm, manufactureform
    
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import ProductTable, Blockchain

from .serializers import *



# Create your views here.
class MainPage(View):
    def get(self, request):
        return render(request, "mainpage.html")
class LoginPage(View): 
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        UserName = request.POST['UserName']
        PassWord = request.POST['PassWord']
        try:
            login_obj = LoginTable.objects.get(UserName=UserName, PassWord=PassWord)
            if login_obj.type == "admin":
                return HttpResponse('''<script>window.location="/AdminDashboardPage/"</script>''')
            elif login_obj.type == "manufacture":
                return HttpResponse('''<script>window.location="/ManufactureDashboardPage/"</script>''')
            else:
                return HttpResponse('''<script>alert('contact admin for approval');window.location="/"</script>''')
        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert('invalid username and password');window.location="/"</script>''')

    
class AddPage(View):
    def get(self,request):
     return render(request,"add.html")
class AdminDashboardPage(View): 
    def get(self, request):
        return render(request, "admindashboard.html")
class ManufactureDashboardPage(View): 
    def get(self, request):
        return render(request, "manufacturedashboard.html")
class ApprovePage(View):
     def get(self, request):
        v=ManufactureTable.objects.all()
        return render(request,'approve.html',{'man':v})
     
class UserReg(View):
     def get(self, request):
        return render(request, "Register.html")
     def post(self, request):
         form = manufactureform(request.POST)
         if form.is_valid():
            c=form.save(commit=False)
            d=LoginTable.objects.create(UserName=request.POST['username'],PassWord=request.POST['password'],type='pending')
            print(d)
            c.LOGINID=d
            c.save()
            return HttpResponse('''<script>alert("registered");window.location=("/")</script>''')
class Manufacture(View):
    def get(self, request):
        return render(request, "manufacture.html")
    def post(self, request):
         print("hhhhh")
         form = manufactureform(request.POST)
         if form.is_valid():
            c=form.save(commit=False)
            d=LoginTable.objects.create(UserName=request.POST['username'],PassWord=request.POST['password'],type='pending')
            c.LOGINID=d
            c.save()
            return HttpResponse('''<script>alert("registered");window.location=("/")</script>''')
class Viewmanufacture(View):
    def get(self,request):
        v=ManufactureTable.objects.all()
        return render(request,'viewmanufacture.html',{'man':v})



class AddProduct(View):
    def get(self, request):
        return render(request, "add.html")

    def post(self, request):
        product_name = request.POST.get("ProductName")
        product_type = request.POST.get("ProductType")
        product_id = request.POST.get("ProductId")
        manufacture_date = request.POST.get("Manufacturedate")
        expiry_date = request.POST.get("Expirydate")
        product_price = request.POST.get("Productprice")
        upload_photo = request.FILES.get("Uplaodphoto")
            # Check if the ProductId already exists
        if ProductTable.objects.filter(ProductId=product_id).exists():
            return HttpResponse(
                '''<script>alert("Product ID already exists!");window.location=("/AddProduct/")</script>'''
            )
            # Save product data to the database
        product = ProductTable(
            ProductId=product_id,
            ProductName=product_name,
            ProductType=product_type,
            Manufacturedate=manufacture_date,
            Expirydate=expiry_date,
            Productprice=product_price,
            Uplaodphoto=upload_photo,
        )
        product.save()

        # Add product data to the blockchain
        product_data = {
            "ProductId": product_id,
            "ProductName": product_name,
            "ProductType": product_type,
            "Manufacturedate": manufacture_date,
            "Expirydate": expiry_date,
            "Productprice": product_price,
        }
        Blockchain.add_block(product_data)

        return HttpResponse(
            '''<script>alert("Product added to blockchain successfully!");window.location=("/ManufactureDashboardPage")</script>'''
        )

import re
class ViewAddProduct(View):
    def get(self, request):
        products = ProductTable.objects.all()
        

        # Extract product names to match with blockchain data
        product_ids = products.values_list("ProductId", flat=True)
        print(product_ids)

        if product_ids:
                # Escape each ProductId to avoid regex issues (e.g., quotes, special chars)
                escaped_product_ids = [re.escape(pid) for pid in product_ids]
                print(escaped_product_ids)

                # Create a regex pattern to match any of the escaped product_ids in the blockchain data
                pattern = r'("ProductId":\s*"(?:' + '|'.join(escaped_product_ids) + ')")'
                print(pattern)
                # Filter blocks whose data field contains any of the product IDs
                blocks = Block.objects.filter(data__regex=pattern)
                print("Blocks:", blocks)
        else:
                blocks = Block.objects.none()

        return render(request, "viewaddproduct.html", {"products": products, "chain": blocks})


class UpdateProduct(View):
    def get(self, request, id):
        product = get_object_or_404(ProductTable, id=id)
        return render(request, "update.html", {"product": product})

    def post(self, request,id):
        product = get_object_or_404(ProductTable, id=id)
        product.ProductName = request.POST.get("ProductName")
        product.ProductType = request.POST.get("ProductType")
        product.Manufacturedate = request.POST.get("Manufacturedate")
        product.Expirydate = request.POST.get("Expirydate")
        product.Productprice = request.POST.get("Productprice")

        if request.FILES.get("Uplaodphoto"):
            product.Uplaodphoto = request.FILES.get("Uplaodphoto")

        product.save()

        return HttpResponse(
            '''<script>alert("Product updated successfully!");window.location=("/ViewAddProduct/")</script>'''
        )


class DeleteProduct(View):
    def get(self, request,id):
        product = get_object_or_404(ProductTable, id=id)
        product.delete()
        return HttpResponse(
            '''<script>alert("Product deleted successfully!");window.location=("/ViewAddProduct/")</script>'''
        )

               




class viewFeedBack(View):
    def get(self,request):
        v=FeedBack.objects.all()
        return render(request,'feedback.html',{'v':v})
    
    


         
class Accept_Man(View):
    def get(self, request, id):
            Cam = ManufactureTable.objects.get(id=id)
            print(Cam)  # Fetch the instance
            Cam.LOGINID.type = 'CameraMan'  # Update the status
            Cam.LOGINID.save()  # Save the changes
            return HttpResponse('''<script>alert("successfully Accepted");window.location="/ApprovePage/"</script>''')  

        

class Reject_Man(View):
    def get(self, request, id):
            Cam = ManufactureTable.objects.get(id=id)  # Fetch the instance
            Cam.LOGINID.type = 'Rejected'  # Update the status
            Cam.LOGINID.save()  # Save the changes
            return HttpResponse('''<script>alert("successfully Rejected");window.location="/ApprovePage/"</script>''')  
        
    

class CheckProductInBlock(APIView):
    def get(self, request, product_id, *args, **kwargs):
        # Iterate through all blocks to check if the product ID exists in the data field
        blocks = Block.objects.all()

        for block in blocks:
            try:
                block_data = json.loads(block.data)  # Parse the block data (assuming it's JSON)
                # Check if the ProductId is in the block data
                if block_data.get("ProductId") == product_id:
                    return Response(
                        {"message": f"Product with ID {product_id} found in block {block.index}."},
                        status=status.HTTP_200_OK,
                    )
            except json.JSONDecodeError:
                # If the block data is not valid JSON, continue to the next block
                continue

        # If no block contains the product ID
        return Response(
            {"message": f"Product with ID {product_id} not found in any block."},
            status=status.HTTP_404_NOT_FOUND,
        )

class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        loginserializer=LoginTableSerializer(data=request.data)
        userserializer = UserTableSerializer(data=request.data)
        
        if loginserializer.is_valid() and userserializer.is_valid():
            # Save the new user
            c=loginserializer.save()
            userserializer.save(LOGINID=c)
            return Response(
                {"message": "User registered successfully", "data": userserializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Error in registration", "errors": userserializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
class Loginapi(APIView):
    def post(self, request):
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(username=username).first()

        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)

        # # Check password using check_password
        # if not check_password(password, t_user.password):
        #     response_dict["message"] = "failed"
        #     return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # Successful login response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id

        return Response(response_dict, status=status.HTTP_200_OK)
    


class FeedBackCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        data['USERID']=UserTable.objects.get(LOGINID__id=request.data['LOGINID']).id
        serializer = FeedBackSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the feedback to the database
            return Response(
                {"message": "Feedback submitted successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error in submitting feedback", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
