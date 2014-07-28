# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Search'
        db.create_table(u'search_search', (
            ('search_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_search_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user_searching', self.gf('django.db.models.fields.related.ForeignKey')(related_name='searches', to=orm['auth.User'])),
            ('explore_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stream_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('yap_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_searched', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('profile_posts_stream_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_likes_stream_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_listens_stream_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hashtags_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('channels_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_handles_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('general_searched_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text_searched', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('is_after_request', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_trending', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_recent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_people', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_searched', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'search', ['Search'])

        # Adding M2M table for field hashtags_searched on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_hashtags_searched')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('hashtag', models.ForeignKey(orm[u'yap.hashtag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'hashtag_id'])

        # Adding M2M table for field channels_searched on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_channels_searched')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('channel', models.ForeignKey(orm[u'yap.channel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'channel_id'])

        # Adding M2M table for field user_handles_searched on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_user_handles_searched')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Search'
        db.delete_table(u'search_search')

        # Removing M2M table for field hashtags_searched on 'Search'
        db.delete_table(db.shorten_name(u'search_search_hashtags_searched'))

        # Removing M2M table for field channels_searched on 'Search'
        db.delete_table(db.shorten_name(u'search_search_channels_searched'))

        # Removing M2M table for field user_handles_searched on 'Search'
        db.delete_table(db.shorten_name(u'search_search_user_handles_searched'))


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
        u'search.search': {
            'Meta': {'ordering': "['-date_searched']", 'object_name': 'Search'},
            'channels_searched': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_searches'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['yap.Channel']"}),
            'channels_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_searched': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explore_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'general_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashtags_searched': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_searches'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['yap.Hashtag']"}),
            'hashtags_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_after_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_people': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_recent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'profile_likes_stream_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_listens_stream_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_posts_stream_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_searched': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'profile_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'search_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stream_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text_searched': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_handles_searched': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_searches'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'user_handles_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_search_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'user_searching': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'searches'", 'to': u"orm['auth.User']"}),
            'yap_searched_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        }
    }

    complete_apps = ['search']