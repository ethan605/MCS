''' chay file nay truoc de nhap tai khoan admin vao database'''

from MCS.system.models import User
admin = User()
admin.username = 'admin'
admin.password = 'admin'
admin.priority = 1
admin.save()