# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('system_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('system', ['User'])

        # Adding model 'Shop'
        db.create_table('system_shop', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['system.User'], unique=True, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('system', ['Shop'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('system_user')

        # Deleting model 'Shop'
        db.delete_table('system_shop')


    models = {
        'system.shop': {
            'Meta': {'object_name': 'Shop', '_ormbases': ['system.User']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['system.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'system.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['system']
