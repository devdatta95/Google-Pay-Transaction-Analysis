from gpay_insights import create_app

server, dash_app = create_app()

if __name__ == "__main__":
    dash_app.run(debug=False, use_reloader=True)
