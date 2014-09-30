# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'location_country', (
            ('country_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_activated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'location', ['Country'])

        # Adding model 'USState'
        db.create_table(u'location_usstate', (
            ('us_states_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('us_state_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('us_state_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_activated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'location', ['USState'])

        # Adding model 'USZIPCode'
        db.create_table(u'location_uszipcode', (
            ('us_zip_code_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('us_zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_activated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'location', ['USZIPCode'])

        # Adding model 'City'
        db.create_table(u'location_city', (
            ('city_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('us_zip_code', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='city_us_zip_code', null=True, to=orm['location.USZIPCode'])),
            ('us_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='city_us_state', null=True, to=orm['location.USState'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='city_country', to=orm['location.Country'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_activated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'location', ['City'])

        # Adding model 'GeographicTarget'
        db.create_table(u'location_geographictarget', (
            ('geographic_target_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geographic_countries_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geographic_states_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geographic_zip_codes_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geographic_cities_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'location', ['GeographicTarget'])

        # Adding M2M table for field geographic_countries on 'GeographicTarget'
        m2m_table_name = db.shorten_name(u'location_geographictarget_geographic_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('geographictarget', models.ForeignKey(orm[u'location.geographictarget'], null=False)),
            ('country', models.ForeignKey(orm[u'location.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['geographictarget_id', 'country_id'])

        # Adding M2M table for field geographic_states on 'GeographicTarget'
        m2m_table_name = db.shorten_name(u'location_geographictarget_geographic_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('geographictarget', models.ForeignKey(orm[u'location.geographictarget'], null=False)),
            ('usstate', models.ForeignKey(orm[u'location.usstate'], null=False))
        ))
        db.create_unique(m2m_table_name, ['geographictarget_id', 'usstate_id'])

        # Adding M2M table for field geographic_zip_codes on 'GeographicTarget'
        m2m_table_name = db.shorten_name(u'location_geographictarget_geographic_zip_codes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('geographictarget', models.ForeignKey(orm[u'location.geographictarget'], null=False)),
            ('uszipcode', models.ForeignKey(orm[u'location.uszipcode'], null=False))
        ))
        db.create_unique(m2m_table_name, ['geographictarget_id', 'uszipcode_id'])

        # Adding M2M table for field geographic_cities on 'GeographicTarget'
        m2m_table_name = db.shorten_name(u'location_geographictarget_geographic_cities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('geographictarget', models.ForeignKey(orm[u'location.geographictarget'], null=False)),
            ('city', models.ForeignKey(orm[u'location.city'], null=False))
        ))
        db.create_unique(m2m_table_name, ['geographictarget_id', 'city_id'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'location_country')

        # Deleting model 'USState'
        db.delete_table(u'location_usstate')

        # Deleting model 'USZIPCode'
        db.delete_table(u'location_uszipcode')

        # Deleting model 'City'
        db.delete_table(u'location_city')

        # Deleting model 'GeographicTarget'
        db.delete_table(u'location_geographictarget')

        # Removing M2M table for field geographic_countries on 'GeographicTarget'
        db.delete_table(db.shorten_name(u'location_geographictarget_geographic_countries'))

        # Removing M2M table for field geographic_states on 'GeographicTarget'
        db.delete_table(db.shorten_name(u'location_geographictarget_geographic_states'))

        # Removing M2M table for field geographic_zip_codes on 'GeographicTarget'
        db.delete_table(db.shorten_name(u'location_geographictarget_geographic_zip_codes'))

        # Removing M2M table for field geographic_cities on 'GeographicTarget'
        db.delete_table(db.shorten_name(u'location_geographictarget_geographic_cities'))


    models = {
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
        }
    }

    complete_apps = ['location']