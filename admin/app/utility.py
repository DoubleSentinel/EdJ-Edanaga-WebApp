from flask import url_for, redirect, abort, request, render_template

from flask_security import current_user

def UserAccessFactory(role):
    class UserAccess:
        def is_accessible(self):
            return (current_user.is_active and
                    current_user.is_authenticated and
                    current_user.has_role(role)
            )

        def _handle_view(self, name, **kwargs):
            """
            Override builtin _handle_view in order to redirect users when a view is not accessible.
            """
            if not self.is_accessible():
                if current_user.is_authenticated:
                    # permission denied
                    abort(403)
                else:
                    # login
                    return redirect(url_for('security.login', next=request.url))

    return UserAccess
