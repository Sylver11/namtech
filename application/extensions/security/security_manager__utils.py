from flask import jsonify

class SecurityManager__Utils(object):

    def _prepare_create_user_args(self, **kwargs):
        """Checking if specified roles exist"""
        roles = kwargs.get("roles", [])
        for i, role in enumerate(roles):
            rn = role.name if isinstance(role, self.role_model) else role
            roles[i] = self.find_role(rn)
        kwargs["roles"] = roles
        return kwargs

    def _json_response(self, status, redirect_addr, desc):
        resp = {}
        resp['status'] = status
        resp['redirect_addr'] = redirect_addr
        resp['desc'] = desc
        return jsonify(resp)
