from operators.models import Provider
from django.contrib.auth.models import User

user = User(username='admin')
user.set_password('admin')
user.is_staff = True
user.is_superuser = True
user.save()
admin = Provider(user=user, name='admin', password='admin')
admin.password=admin.encrypt()
admin.save()