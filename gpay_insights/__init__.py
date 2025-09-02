from pathlib import Path
from flask import Flask
import dash
from . import config
from .data_loader import load_data_context
from .layouts.base import apply_index_string
from .layouts.dashboard import build_layout
from .callbacks.sync import register_sync_callbacks
from .callbacks.main import register_main_callbacks
from .callbacks.merchant import register_merchant_callbacks
from .callbacks.downloads import register_download_callbacks

def create_app(data_path: Path | None = None):
    server = Flask(__name__)

    # load + attach data context once
    ctx = load_data_context(data_path or config.DATA_FILE)
    server.config["DATACTX"] = ctx

    dash_app = dash.Dash(
        __name__,
        server=server,
        title="Google Pay Dashboard — Light",
        external_stylesheets=config.EXTERNAL_STYLESHEETS,
        suppress_callback_exceptions=True,
    )

    apply_index_string(dash_app)              # header/nav/footer
    dash_app.layout = build_layout(ctx)       # components

    # callbacks
    register_sync_callbacks(dash_app, ctx)
    register_main_callbacks(dash_app, ctx)
    register_merchant_callbacks(dash_app, ctx)
    register_download_callbacks(dash_app, ctx)

    return server, dash_app
