# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Report'
        db.create_table(u'report_report', (
            ('report_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_report_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reported', to=orm['auth.User'])),
            ('reported_yap_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reported_yap', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reports', null=True, to=orm['yap.Yap'])),
            ('reported_reyap_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reported_reyap', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reports', null=True, to=orm['yap.Reyap'])),
            ('reported_user_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reported_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reports', null=True, to=orm['auth.User'])),
            ('reported_bug_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reported_general_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('contact_phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('datetime_reported', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'report', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Report'
        db.delete_table(u'report_report')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'location.city': {
            'Meta': {'object_name': 'City'},
            'city_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'city_country'", 'to': u"orm['location.Country']"}),
            'date_activated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'us_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'city_us_state'", 'null': 'True', 'to': u"orm['location.USState']"}),
            'us_zip_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'city_us_zip_code'", 'null': 'True', 'to': u"orm['location.USZIPCode']"})
        },
        u'location.country': {
            'Meta': {'object_name': 'Country'},
            'country_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_activated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'location.geographictarget': {
            'Meta': {'object_name': 'GeographicTarget'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geographic_cities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'geographic_cities'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['location.City']"}),
            'geographic_cities_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geographic_countries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'geographic_countries'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['location.Country']"}),
            'geographic_countries_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geographic_states': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'geographic_states'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['location.USState']"}),
            'geographic_states_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geographic_target_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'geographic_zip_codes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'geographic_zip_codes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['location.USZIPCode']"}),
            'geographic_zip_codes_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'location.usstate': {
            'Meta': {'object_name': 'USState'},
            'date_activated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'us_state_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'us_state_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'us_states_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'location.uszipcode': {
            'Meta': {'object_name': 'USZIPCode'},
            'date_activated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'us_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'us_zip_code_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'report.report': {
            'Meta': {'object_name': 'Report'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'contact_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'datetime_reported': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'report_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reported_bug_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_general_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_reyap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reports'", 'null': 'True', 'to': u"orm['yap.Reyap']"}),
            'reported_reyap_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reports'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'reported_user_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_yap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reports'", 'null': 'True', 'to': u"orm['yap.Yap']"}),
            'reported_yap_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reported'", 'to': u"orm['auth.User']"}),
            'user_report_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        u'yap.channel': {
            'Meta': {'object_name': 'Channel'},
            'channel_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'channel_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'channel_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geographic_target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.GeographicTarget']", 'null': 'True', 'blank': 'True'}),
            'icon_explore_path_clicked': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'icon_explore_path_unclicked': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'icon_yap_path_clicked': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'icon_yap_path_unclicked': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_bonus_channel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_promoted': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'yap.hashtag': {
            'Meta': {'object_name': 'Hashtag'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hashtag_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'hashtag_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'yap.reyap': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Reyap'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_plus_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'google_plus_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_unreyapped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'like_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'linkedin_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'listen_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reyap_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'reyap_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reyap_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reyap_reyap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reyaps'", 'null': 'True', 'to': u"orm['yap.Reyap']"}),
            'twitter_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unreyapped_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reyaps'", 'to': u"orm['auth.User']"}),
            'user_reyap_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'yap': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reyaps'", 'to': u"orm['yap.Yap']"})
        },
        u'yap.yap': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Yap'},
            'audio_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'yaps'", 'null': 'True', 'to': u"orm['yap.Channel']"}),
            'channel_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_shared_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_plus_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'google_plus_shared_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashtags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'yaps'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['yap.Hashtag']"}),
            'hashtags_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.BigIntegerField', [], {}),
            'like_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'linkedin_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_shared_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'listen_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'picture_cropped_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture_cropped_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'picture_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'reyap_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_shared_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'yaps'", 'to': u"orm['auth.User']"}),
            'user_tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'yaps_in'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'user_tags_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_yap_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'web_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'web_link_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'yap_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['report']