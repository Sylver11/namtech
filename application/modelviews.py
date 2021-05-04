from flask import redirect, url_for, abort
from flask_admin.contrib import sqla
from flask_security import current_user


class AdminModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role(['overlord', 'admin'])
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('flask_security_bp.login', next=request.url))
