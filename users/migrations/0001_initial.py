# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DeactivatedUserLog'
        db.create_table(u'users_deactivateduserlog', (
            ('deactivated_user_log_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_deactivated_user_log_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deactivate_user_logs', to=orm['auth.User'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['DeactivatedUserLog'])

        # Adding model 'BlackList'
        db.create_table(u'users_blacklist', (
            ('blacklist_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('account_created_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('account_created_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('blacklisted_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'users', ['BlackList'])

        # Adding model 'Profile'
        db.create_table(u'users_profile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, primary_key=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('follower_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('following_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('yap_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('like_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('listen_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('reyap_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('profile_picture_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_picture_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('profile_picture_cropped_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_picture_cropped_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('user_city', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile_user_city', null=True, to=orm['location.City'])),
            ('user_us_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile_user_state', null=True, to=orm['location.USState'])),
            ('user_us_zip_code', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile_user_zip_code', null=True, to=orm['location.USZIPCode'])),
            ('user_country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile_user_country', null=True, to=orm['location.Country'])),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('high_security_account_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified_account_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('listen_stream_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('posts_are_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['Profile'])

        # Adding model 'UserInfo'
        db.create_table(u'users_userinfo', (
            ('user_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('user_city', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_city', null=True, to=orm['location.City'])),
            ('user_us_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_state', null=True, to=orm['location.USState'])),
            ('user_us_zip_code', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_zip_code', null=True, to=orm['location.USZIPCode'])),
            ('user_country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_country', null=True, to=orm['location.Country'])),
            ('last_account_modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('high_security_account_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified_account_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('facebook_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('twitter_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('twitter_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('google_plus_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_plus_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('google_plus_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('linkedin_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('linkedin_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('profile_picture_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_picture_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('profile_picture_cropped_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_picture_cropped_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('listen_stream_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('posts_are_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('notify_for_mentions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_reyaps', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_likes', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_new_followers', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_yapster', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user_created_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('user_created_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('user_created_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_deleted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['UserInfo'])

        # Adding model 'Settings'
        db.create_table(u'users_settings', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='settings', unique=True, primary_key=True, to=orm['auth.User'])),
            ('notify_for_mentions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_reyaps', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_likes', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_listens', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_new_followers', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_for_yapster', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('facebook_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('facebook_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('twitter_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_plus_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_plus_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('google_plus_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('linkedin_share_reyap', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['Settings'])

        # Adding model 'Recommended'
        db.create_table(u'users_recommended', (
            ('recommendation_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_recommendation_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recommended', to=orm['auth.User'])),
            ('date_recommended', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_will_be_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('geographic_target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.GeographicTarget'], null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['Recommended'])

        # Adding model 'ForgotPasswordRequest'
        db.create_table(u'users_forgotpasswordrequest', (
            ('forgot_password_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_forgot_password_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forgot_password_requests', to=orm['auth.User'])),
            ('user_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('reset_password_security_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('reset_password_security_code_used_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_used', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user_signed_in_after_without_using_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_signed_in_without_using', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('forgot_password_request_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('forgot_password_request_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('forgot_password_request_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'users', ['ForgotPasswordRequest'])

        # Adding model 'UserFunctions'
        db.create_table(u'users_userfunctions', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='functions', unique=True, primary_key=True, to=orm['auth.User'])),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'users', ['UserFunctions'])

        # Adding model 'SessionVerification'
        db.create_table(u'users_sessionverification', (
            ('session_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_session_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['auth.User'])),
            ('session_device_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('session_manually_closed_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('session_logged_out_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('session_timed_out_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('session_created_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sesssion_created_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('session_created_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'users', ['SessionVerification'])


    def backwards(self, orm):
        # Deleting model 'DeactivatedUserLog'
        db.delete_table(u'users_deactivateduserlog')

        # Deleting model 'BlackList'
        db.delete_table(u'users_blacklist')

        # Deleting model 'Profile'
        db.delete_table(u'users_profile')

        # Deleting model 'UserInfo'
        db.delete_table(u'users_userinfo')

        # Deleting model 'Settings'
        db.delete_table(u'users_settings')

        # Deleting model 'Recommended'
        db.delete_table(u'users_recommended')

        # Deleting model 'ForgotPasswordRequest'
        db.delete_table(u'users_forgotpasswordrequest')

        # Deleting model 'UserFunctions'
        db.delete_table(u'users_userfunctions')

        # Deleting model 'SessionVerification'
        db.delete_table(u'users_sessionverification')


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
        u'users.blacklist': {
            'Meta': {'object_name': 'BlackList'},
            'account_created_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'account_created_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blacklist_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'blacklisted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'users.deactivateduserlog': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'DeactivatedUserLog'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deactivated_user_log_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deactivate_user_logs'", 'to': u"orm['auth.User']"}),
            'user_deactivated_user_log_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        u'users.forgotpasswordrequest': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'ForgotPasswordRequest'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_signed_in_without_using': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_used': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'forgot_password_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'forgot_password_request_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'forgot_password_request_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'forgot_password_request_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reset_password_security_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reset_password_security_code_used_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forgot_password_requests'", 'to': u"orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user_forgot_password_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'user_signed_in_after_without_using_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'follower_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'following_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'high_security_account_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'like_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'listen_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'listen_stream_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'posts_are_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_picture_cropped_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_picture_cropped_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'profile_picture_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_picture_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'reyap_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"}),
            'user_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_user_city'", 'null': 'True', 'to': u"orm['location.City']"}),
            'user_country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_user_country'", 'null': 'True', 'to': u"orm['location.Country']"}),
            'user_us_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_user_state'", 'null': 'True', 'to': u"orm['location.USState']"}),
            'user_us_zip_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_user_zip_code'", 'null': 'True', 'to': u"orm['location.USZIPCode']"}),
            'verified_account_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'yap_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'users.recommended': {
            'Meta': {'object_name': 'Recommended'},
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_recommended': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_will_be_deactivated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geographic_target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.GeographicTarget']", 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recommendation_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recommended'", 'to': u"orm['auth.User']"}),
            'user_recommendation_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        u'users.sessionverification': {
            'Meta': {'object_name': 'SessionVerification'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'session_created_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'session_created_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'session_device_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'session_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_logged_out_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session_manually_closed_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session_timed_out_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sesssion_created_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': u"orm['auth.User']"}),
            'user_session_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        u'users.settings': {
            'Meta': {'object_name': 'Settings'},
            'facebook_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_plus_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'google_plus_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_plus_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notify_for_likes': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_listens': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_new_followers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_reyaps': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_yapster': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'twitter_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'users.userfunctions': {
            'Meta': {'object_name': 'UserFunctions'},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'functions'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'users.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'facebook_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'google_plus_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'google_plus_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_plus_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'high_security_account_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_account_modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'linkedin_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'listen_stream_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_likes': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_mentions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_new_followers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_reyaps': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_for_yapster': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'posts_are_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_picture_cropped_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_picture_cropped_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'profile_picture_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_picture_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitter_account_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_connection_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter_share_reyap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_city'", 'null': 'True', 'to': u"orm['location.City']"}),
            'user_country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_country'", 'null': 'True', 'to': u"orm['location.Country']"}),
            'user_created_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user_created_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user_created_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'user_deleted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'user_us_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_state'", 'null': 'True', 'to': u"orm['location.USState']"}),
            'user_us_zip_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_zip_code'", 'null': 'True', 'to': u"orm['location.USZIPCode']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'verified_account_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['users']