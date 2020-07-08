import os, re, glob, datetime

from flask import url_for, render_template, render_template_string, redirect, request, flash

from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView, EmbeddedForm

from wtforms import TextAreaField, SelectField, HiddenField, MultipleFileField, FileField
from wtforms.widgets import TextArea

from .models import (
    UIText,
    Conversation,
    Scene)

from utility import UserAccessFactory


# These classes serve as an override for the Flask-Admin TextArea views.
# If the tag "markdownEditor" is present in the class of a TextArea tag in html,
# it will be replaced by a Markdown Editor (SimpleMDE)
class SimpleMDETextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        try:
            kwargs['class'] += ' markdownEditor'
        except KeyError:
            kwargs['class'] = 'markdownEditor'
        return super(SimpleMDETextAreaWidget, self).__call__(field, **kwargs)


class SimpleMDETextAreaField(TextAreaField):
    widget = SimpleMDETextAreaWidget()


# Model views for Flask-Admin
class UITextView(UserAccessFactory('user'), ModelView):
    # can_create = False
    # can_delete = False

    column_list = [
        "target_ui_name",
        "language",
        "description",
        "text",
    ]

    # column_default_sort = [('archived', False), ('priority', True), ('title', False)]

    # create_template = 'admin/create/project.html'
    # edit_template = 'admin/edit/project.html'

    # form_overrides = {
    #     'description': SimpleMDETextAreaField
    # }

    form_args = {
        'target_ui_name': {
            'label': "Identifier for the target UI element in Unity.",
        },
        'language': {
            'label': "Language of the UI element text",
        },
        'description': {
            'label': "Description to access the UI element on the game",
        },
        'text': {
            'label': "UI element's text'",
        },
    }

    column_labels = {
        'target_ui_name': "UI identifier",
        'language': "Language of the UI",
        'description': "Where the UI element is",
        'text': "UI element's text",
    }


class ConversationView(EmbeddedForm):
    # can_create = False
    # can_delete = False

    form_overrides = {
        'text': SimpleMDETextAreaField
    }

    form_args = {
        'target_character': {
            'label': "Identifier of the speaking character",
        },
        'position_in_conversation': {
            'label': "Ordering position of the conversation snippet",
        },
        'text': {
            'label': "Contents of the conversation's snippet",
        },
    }

    column_labels = {
        'target_character': "Character",
        'language': "Language",
        'text': "Text",
    }


class SceneView(UserAccessFactory('user'), ModelView):
    # can_create = False
    # can_delete = False

    column_list = [
        "unity_scene_name",
        "language",
    ]

    # create_template = 'admin/create/project.html'
    # edit_template = 'admin/edit/project.html'
    extra_css = ["https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css"]
    extra_js = ['http://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
                '/static/custom.JS']

    form_args = {
        'unity_scene_name': {
            'label': "Target Unity Scene",
        },
        'language': {
            'label': "Language version",
        },
        'conversation': {
            'label': "Conversation",
        },
    }
    form_subdocuments = {
        'conversation': {
            'form_subdocuments': {
                None: ConversationView(),
            }
        }
    }
    column_labels = {
        'unity_scene_name': "Target Unity Scene",
        'language': "Language",
    }
