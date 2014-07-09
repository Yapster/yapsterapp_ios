# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hashtag'
        db.create_table(u'yap_hashtag', (
            ('hashtag_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hashtag_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_blocked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'yap', ['Hashtag'])

        # Adding model 'Channel'
        db.create_table(u'yap_channel', (
            ('channel_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('channel_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('icon_explore_path_clicked', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('icon_explore_path_unclicked', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('icon_yap_path_clicked', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('icon_yap_path_unclicked', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('is_bonus_channel', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_promoted', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('geographic_target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.GeographicTarget'], null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'yap', ['Channel'])

        # Adding model 'Yap'
        db.create_table(u'yap_yap', (
            ('yap_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_yap_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='yaps', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('hashtags_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('channel_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='yaps', null=True, to=orm['yap.Channel'])),
            ('user_tags_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('length', self.gf('django.db.models.fields.BigIntegerField')()),
            ('listen_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('reyap_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('like_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('web_link_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('web_link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('audio_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('picture_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('picture_path', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('picture_cropped_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('picture_cropped_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('facebook_shared_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('twitter_shared_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('google_plus_shared_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_plus_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('linkedin_shared_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'yap', ['Yap'])

        # Adding M2M table for field hashtags on 'Yap'
        m2m_table_name = db.shorten_name(u'yap_yap_hashtags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('yap', models.ForeignKey(orm[u'yap.yap'], null=False)),
            ('hashtag', models.ForeignKey(orm[u'yap.hashtag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['yap_id', 'hashtag_id'])

        # Adding M2M table for field user_tags on 'Yap'
        m2m_table_name = db.shorten_name(u'yap_yap_user_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('yap', models.ForeignKey(orm[u'yap.yap'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['yap_id', 'user_id'])

        # Adding model 'Reyap'
        db.create_table(u'yap_reyap', (
            ('reyap_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_reyap_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('yap', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reyaps', to=orm['yap.Yap'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reyaps', to=orm['auth.User'])),
            ('reyap_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reyap_reyap', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reyaps', null=True, to=orm['yap.Reyap'])),
            ('facebook_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('twitter_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('google_plus_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_plus_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('linkedin_connection_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin_account_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('reyap_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('like_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('listen_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('is_unreyapped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unreyapped_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'yap', ['Reyap'])

        # Adding model 'Like'
        db.create_table(u'yap_like', (
            ('like_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_like_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('yap', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['yap.Yap'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['auth.User'])),
            ('reyap_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reyap', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='likes', null=True, to=orm['yap.Reyap'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_unliked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unliked_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'yap', ['Like'])

        # Adding model 'Listen'
        db.create_table(u'yap_listen', (
            ('listen_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_listen_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='listens', to=orm['auth.User'])),
            ('yap', self.gf('django.db.models.fields.related.ForeignKey')(related_name='listens', to=orm['yap.Yap'])),
            ('reyap_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reyap', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='listens', null=True, to=orm['yap.Reyap'])),
            ('listen_click_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_listened', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'yap', ['Listen'])

        # Adding model 'ListenClick'
        db.create_table(u'yap_listenclick', (
            ('listen_click_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_listen_click_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_listen_clicked', to=orm['auth.User'])),
            ('listen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='listen_clicked', to=orm['yap.Listen'])),
            ('hashtag_clicked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hashtag_clicked', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='listen_clicked', null=True, to=orm['yap.Hashtag'])),
            ('user_handle_clicked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_handle_clicked', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='listen_handle_clicked', null=True, to=orm['auth.User'])),
            ('user_yapped_clicked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_reyapped_clicked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('web_link_clicked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('picture_clicked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('skipped_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('liked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unliked_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('liked_like', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='listens_liked', null=True, to=orm['yap.Like'])),
            ('reyapped_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unreyapped_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reyapped_reyap', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='listens_reyapped', null=True, to=orm['yap.Reyap'])),
            ('time_clicked', self.gf('django.db.models.fields.BigIntegerField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'yap', ['ListenClick'])

        # Adding model 'FollowerRequest'
        db.create_table(u'yap_followerrequest', (
            ('follower_request_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_follower_request_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requests', to=orm['auth.User'])),
            ('user_requested', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requested', to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_unrequested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_unrequested', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_accepted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_denied', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_denied', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_unfollowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_unfollowed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'yap', ['FollowerRequest'])


    def backwards(self, orm):
        # Deleting model 'Hashtag'
        db.delete_table(u'yap_hashtag')

        # Deleting model 'Channel'
        db.delete_table(u'yap_channel')

        # Deleting model 'Yap'
        db.delete_table(u'yap_yap')

        # Removing M2M table for field hashtags on 'Yap'
        db.delete_table(db.shorten_name(u'yap_yap_hashtags'))

        # Removing M2M table for field user_tags on 'Yap'
        db.delete_table(db.shorten_name(u'yap_yap_user_tags'))

        # Deleting model 'Reyap'
        db.delete_table(u'yap_reyap')

        # Deleting model 'Like'
        db.delete_table(u'yap_like')

        # Deleting model 'Listen'
        db.delete_table(u'yap_listen')

        # Deleting model 'ListenClick'
        db.delete_table(u'yap_listenclick')

        # Deleting model 'FollowerRequest'
        db.delete_table(u'yap_followerrequest')


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
        u'yap.followerrequest': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'FollowerRequest'},
            'date_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_denied': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_unfollowed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_unrequested': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'follower_request_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_denied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_unfollowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_unrequested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requests'", 'to': u"orm['auth.User']"}),
            'user_follower_request_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'user_requested': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requested'", 'to': u"orm['auth.User']"})
        },
        u'yap.hashtag': {
            'Meta': {'object_name': 'Hashtag'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hashtag_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'hashtag_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'yap.like': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Like'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_unliked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'like_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reyap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'to': u"orm['yap.Reyap']"}),
            'reyap_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unliked_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes'", 'to': u"orm['auth.User']"}),
            'user_like_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'yap': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes'", 'to': u"orm['yap.Yap']"})
        },
        u'yap.listen': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Listen'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'listen_click_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'listen_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reyap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'listens'", 'null': 'True', 'to': u"orm['yap.Reyap']"}),
            'reyap_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_listened': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'listens'", 'to': u"orm['auth.User']"}),
            'user_listen_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'yap': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'listens'", 'to': u"orm['yap.Yap']"})
        },
        u'yap.listenclick': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'ListenClick'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hashtag_clicked': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'listen_clicked'", 'null': 'True', 'to': u"orm['yap.Hashtag']"}),
            'hashtag_clicked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'liked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'liked_like': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'listens_liked'", 'null': 'True', 'to': u"orm['yap.Like']"}),
            'listen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'listen_clicked'", 'to': u"orm['yap.Listen']"}),
            'listen_click_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture_clicked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reyapped_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reyapped_reyap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'listens_reyapped'", 'null': 'True', 'to': u"orm['yap.Reyap']"}),
            'skipped_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_clicked': ('django.db.models.fields.BigIntegerField', [], {}),
            'unliked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unreyapped_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_listen_clicked'", 'to': u"orm['auth.User']"}),
            'user_handle_clicked': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'listen_handle_clicked'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_handle_clicked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_listen_click_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'user_reyapped_clicked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_yapped_clicked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'web_link_clicked_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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

    complete_apps = ['yap']