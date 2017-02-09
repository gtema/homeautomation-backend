from homeautomation import create_app

app = create_app()

if __name__ == "__main__":
    port = int(app.config.get('PORT'))
    app.logger.info('Starting listening on port=%d', port)
    app.run(host='0.0.0.0', port=port)
