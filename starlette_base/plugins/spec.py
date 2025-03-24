import logging

from spectree import SpecTree
from spectree.page import PAGE_TEMPLATES

SPECTREE_CONFIG = {"path": "/apidocs", "annotations": False}


class SpecTreePlugin:
    def __init__(self, config_name="SPECTREE_CONFIG", **kwargs):
        self._config_name = config_name
        self._spec = SpecTree("starlette", **kwargs)
        self._initialized = False

    def register(self, app):
        if self._initialized:
            return self._spec

        self._spec.register(app)
        self._initialized = True
        logging.warning("--- SpecTree initialized.")
        return self._spec

    @property
    def spec(self) -> SpecTree:
        return self._spec


PAGE_TEMPLATES[
    "swagger"
] = """
<!-- HTML for static distribution bundle build -->
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="SwaggerUI"/>
        <title>SwaggerUI</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%221em%22 font-size=%2280%22>📄</text></svg>">
    </head>

    <body>
        <div id="swagger-ui"></div>

        <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" crossorigin></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-standalone-preset.js" crossorigin></script>
        <script>
        window.onload = function() {{
        var full = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
        // Begin Swagger UI call region
        const ui = SwaggerUIBundle({{
            url: "{spec_url}",
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            layout: "StandaloneLayout",
            oauth2RedirectUrl: full + "/{spec_path}/swagger/oauth2-redirect.html",
        }});
        ui.initOAuth({{
            clientId: "{client_id}",
            clientSecret: "{client_secret}",
            realm: "{realm}",
            appName: "{app_name}",
            scopeSeparator: "{scope_separator}",
            additionalQueryStringParams: {additional_query_string_params},
            useBasicAuthenticationWithAccessCodeGrant: {use_basic_authentication_with_access_code_grant},
            usePkceWithAuthorizationCodeGrant: {use_pkce_with_authorization_code_grant},
        }});
        // End Swagger UI call region

        window.ui = ui;
        }}
    </script>
    </body>
</html>"""
