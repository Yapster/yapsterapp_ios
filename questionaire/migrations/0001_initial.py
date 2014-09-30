# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionType'
        db.create_table(u'questionaire_questiontype', (
            ('question_type_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_type_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('question_type_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'questionaire', ['QuestionType'])

        # Adding model 'QuestionPossibleAnswer'
        db.create_table(u'questionaire_questionpossibleanswer', (
            ('question_possible_answer_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_possible_answer_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'questionaire', ['QuestionPossibleAnswer'])

        # Adding model 'Question'
        db.create_table(u'questionaire_question', (
            ('question_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionaire.QuestionType'])),
            ('question_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('no_yaps_in_stream_questionaire_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'questionaire', ['Question'])

        # Adding M2M table for field question_possible_answers on 'Question'
        m2m_table_name = db.shorten_name(u'questionaire_question_question_possible_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'questionaire.question'], null=False)),
            ('questionpossibleanswer', models.ForeignKey(orm[u'questionaire.questionpossibleanswer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'questionpossibleanswer_id'])

        # Adding model 'Answer'
        db.create_table(u'questionaire_answer', (
            ('answer_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_answer_id', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['auth.User'])),
            ('chosen_answer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['questionaire.QuestionPossibleAnswer'])),
            ('answer_rank_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('answer_rank', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['questionaire.Question'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_user_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'questionaire', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'QuestionType'
        db.delete_table(u'questionaire_questiontype')

        # Deleting model 'QuestionPossibleAnswer'
        db.delete_table(u'questionaire_questionpossibleanswer')

        # Deleting model 'Question'
        db.delete_table(u'questionaire_question')

        # Removing M2M table for field question_possible_answers on 'Question'
        db.delete_table(db.shorten_name(u'questionaire_question_question_possible_answers'))

        # Deleting model 'Answer'
        db.delete_table(u'questionaire_answer')


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
        u'questionaire.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'answer_rank': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'answer_rank_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chosen_answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['questionaire.QuestionPossibleAnswer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['questionaire.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['auth.User']"}),
            'user_answer_id': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        u'questionaire.question': {
            'Meta': {'object_name': 'Question'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'no_yaps_in_stream_questionaire_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_possible_answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['questionaire.QuestionPossibleAnswer']", 'null': 'True', 'blank': 'True'}),
            'question_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionaire.QuestionType']"})
        },
        u'questionaire.questionpossibleanswer': {
            'Meta': {'object_name': 'QuestionPossibleAnswer'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question_possible_answer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_possible_answer_text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'questionaire.questiontype': {
            'Meta': {'object_name': 'QuestionType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question_type_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_type_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['questionaire']