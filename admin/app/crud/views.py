import os, re, glob, datetime

from flask import url_for, render_template, render_template_string, redirect, request, flash

from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView, EmbeddedForm

from wtforms import TextAreaField, SelectField, HiddenField, MultipleFileField, FileField
from wtforms.widgets import TextArea

from .models import (
    UITranslations,
    UIElement,
    Conversation,
    Scene,
    HomeScreen,
    Invitations
)

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


# Embedded forms for Flask-Admin
class UIElementView(EmbeddedForm):
    # can_create = False
    # can_delete = False

    form_args = {
        'gameobject_id': {
            'label': "Name of the GameObject in Unity",
        },
        'description': {
            'label': "Location of the UIElement",
        },
        'text_value': {
            'label': "Text written on the UIElement",
        },
    }

    form_widget_args = {
        'gameobject_id': {
            'disabled': True
        }
    }

    column_labels = {
        'gameobject_id': "Character",
        'description': "Language",
        'text_value': "Text",
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

    form_widget_args = {
        'target_character': {
            'disabled': True
        }
    }

    column_labels = {
        'target_character': "Character",
        'language': "Language",
        'text': "Text",
    }


# Model views for Flask-Admin
class LanguagesView(UserAccessFactory('superuser'), ModelView):
    pass


class ObjectiveView(UserAccessFactory('superuser'), ModelView):
    can_delete = False
    can_create = False

    form_widget_args = {
        'unity_name': {
            'disabled': True
        }
    }


class ConstantVariablesView(UserAccessFactory('user'), ModelView):
    form_args = {
        'name': {
            'label': "Name of variable set",
        },
        'variable_set': {
            'label': "Set of variables",
        },
    }


class UITranslationsView(UserAccessFactory('user'), ModelView):
    # can_create = False
    can_delete = False

    column_list = [
        "language",
        "scene",
    ]

    # column_default_sort = [('archived', False), ('priority', True), ('title', False)]

    # create_template = 'admin/create/project.html'
    # edit_template = 'admin/edit/project.html'

    form_args = {
        'language': {
            'label': "UI Language",
        },
        'scene': {
            'label': "Scene for this specific group of UI elements",
        },
        'elements': {
            'label': "UI Element in the scene",
        },
    }

    form_subdocuments = {
        'elements': {
            'form_subdocuments': {
                None: UIElementView(),
            }
        }
    }

    form_widget_args = {
        'scene': {
            'disabled': True
        }
    }

    column_labels = {
        'language': "Language of the UI",
        'scene': "Scene for this specific group of UI elements",
    }


class SceneView(UserAccessFactory('user'), ModelView):
    # can_create = False
    # can_delete = False
    column_searchable_list = ['conversation_title']
    # column_filters = ['language']

    column_list = [
        "conversation_title",
        "language",
    ]

    # create_template = 'admin/create/project.html'
    # edit_template = 'admin/edit/project.html'
    extra_css = ["https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css"]
    extra_js = ['http://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
                '/static/custom.JS']

    form_args = {
        'conversation_title': {
            'label': "Title of the conversation",
        },
        'language': {
            'label': "Language version",
        },
        'conversation_content': {
            'label': "Conversation",
        },
    }
    form_subdocuments = {
        'conversation_content': {
            'form_subdocuments': {
                None: ConversationView(),
            }
        }
    }
    form_widget_args = {
        'conversation_title': {
            'disabled': True
        }
    }
    column_labels = {
        'conversation_title': "Title of the conversation",
        'language': "Language",
    }


class HomeScreenView(UserAccessFactory('superuser'), ModelView):
    # can_create = False
    # can_delete = False

    column_list = [
        "language",
    ]

    form_args = {
        'language': {
            'label': "Language of the home screen",
        },
        'welcome_title': {
            'label': "Text shown as a header on the home screen",
        },
        'welcome_text': {
            'label': "Text shown below the title on the home screen",
        },
    }


class InvitationsView(UserAccessFactory('user'), ModelView):
    column_list = [
        "token_url",
        "active",
    ]

    form_args = {
        'token_url': {
            'label': "Token",
        },
        'active': {
            'label': "Is the token active?",
        },
    }

    form_widget_args = {
        'participants': {
            'disabled': True
        }
    }

    def on_model_delete(self, model):
        for participant in model.participants:
            participant.delete()
