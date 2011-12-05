''' chay file nay truoc de nhap tai khoan admin vao database'''

from MCS.system.models import User
admin = User()
admin.username = 'test'
admin.password = 'test'
admin.priority = 2
admin.save()