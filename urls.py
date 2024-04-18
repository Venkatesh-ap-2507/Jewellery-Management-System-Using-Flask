from main import app
import category as cat
import product as product
import adminLogin as ad
import user
from user import contact_us, about_us, my_orders, viewWishlist, addToWishlist

#urls for category
app.add_url_rule("/showAllcategory",view_func=cat.showAllcategory)
app.add_url_rule("/addCategory",view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule("/deleteCategory/<id>",view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule("/editCategory/<id>",view_func=cat.editCategory,methods=["GET","POST"])

#urls for product
app.add_url_rule("/addProduct",view_func=product.addProduct,methods=["GET","POST"])
app.add_url_rule("/showAllproduct",view_func=product.showAllproduct)
app.add_url_rule("/deleteproduct/<product_id>", view_func=product.deleteproduct, methods=["GET", "POST"])
app.add_url_rule("/editproduct/<product_id>", view_func=product.editproduct, methods=["GET", "POST"])

#urls for admin
app.add_url_rule("/adminLogin",view_func=ad.login, methods = ["GET" ,"POST"] )
app.add_url_rule("/adminHome",view_func=ad.adminHome)

#urls for user
app.add_url_rule("/",view_func=user.homepage)
app.add_url_rule("/showproduct/<product_id>",view_func=user.showproduct)

app.add_url_rule("/Login",view_func=user.Login,methods = ["GET" ,"POST"])
app.add_url_rule("/Logout",view_func=user.Logout)
app.add_url_rule("/Register",view_func=user.Register,methods = ["GET" ,"POST"])
app.add_url_rule("/ViewDetails/<product_id>",view_func=user.ViewDetails,methods = ["GET" ,"POST"])
app.add_url_rule("/ShowCart",view_func=user.showCartItems,methods=["GET","POST"])
app.add_url_rule("/MakePayment",view_func=user.MakePayment,methods=["GET","POST"])


# Add URL rules for About Us and Contact Us pages
app.add_url_rule("/about", view_func=about_us)
app.add_url_rule("/contact", view_func=contact_us)

app.add_url_rule("/MyOrders", view_func=my_orders)

app.add_url_rule("/addToWishlist/<product_id>", view_func=addToWishlist)
app.add_url_rule("/viewWishlist", view_func=viewWishlist)
