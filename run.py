from homeautomation import create_app

app = create_app()

if __name__ == "__main__":
    port = app.config.get('PORT')
    app.run(host='0.0.0.0', port=port)
