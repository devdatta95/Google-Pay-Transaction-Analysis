def apply_index_string(app):
    app.index_string = f"""
    <!DOCTYPE html>
    <html>
      <head>
        {{%metas%}}
        <title>Google Pay Transaction Dashboard</title>
        {{%favicon%}}
        {{%css%}}
        <style>
          body {{ margin:0; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto; background:#fff; }}
          .topnav {{ position:sticky; top:0; z-index:1000; display:flex; align-items:center; gap:18px; padding:10px 14px; border-bottom:1px solid #eee; background:#ffffff; }}
          .brand {{ font-weight:700; font-size:18px; }}
          .navlink {{ text-decoration:none; color:#111; border:1px solid #e6e6e6; border-radius:999px; padding:6px 10px; }}
          .navlink:hover {{ background:#f7f7f7; }}
          footer.site-footer {{ padding:16px 12px 26px; border-top:1px solid #eee; background:#fafafa; text-align:center; margin-top:24px; }}
          footer.site-footer a {{ color:#111; margin:0 6px; font-size:18px; }}
          .fa-drupal {{ font-size:46px; color:red; text-shadow:2px 2px 4px #000; }}
          .date-controls {{ display:flex; align-items:flex-end; gap:14px; flex-wrap:wrap; margin:6px 12px; }}
          .date-group {{ display:flex; flex-direction:column; gap:4px; }}
          .date-input {{ border:1px solid #ddd; border-radius:10px; padding:8px 10px; min-width:180px; }}
        </style>
      </head>
      <body>
        <div class="topnav">
            <div class="brand">Google Pay Transaction – Insights</div>
            <a class="navlink" href="#overview">Overview</a>
            <a class="navlink" href="#cats_merch">Categories & Merchants</a>
            <a class="navlink" href="#forecast">Forecast</a>
            <a class="navlink" href="#rfm">RFM</a>
            <a class="navlink" href="#merchant_explorer">Merchant Explorer</a>
            
        </div>
        {{%app_entry%}}
        <footer class="site-footer">
            <p>Find me on social media.</p>
            <p>
                <a href="" target="_blank"><i class="fa fa-facebook w3-hover-opacity"></i></a>
                <a href="https://www.instagram.com/dev_.2422/" target="_blank"><i class="fa fa-instagram w3-hover-opacity"></i></a>
                <a href="https://github.com/devdatta95" target="_blank"><i class="fa fa-github w3-hover-opacity"></i></a>
                <a href="" target="_blank"><i class="fa fa-twitter w3-hover-opacity"></i></a>
                <a href="https://www.linkedin.com/in/devdatta-supnekar/" target="_blank"><i class="fa fa-linkedin w3-hover-opacity"></i></a>
            </p>
            <p>Made by Devdatta Supnekar</p>
            <i class="fa fa-drupal w3-hover-opacity"></i>
        </footer>
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
      </body>
    </html>
    """
