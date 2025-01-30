from nuri import create_app

app = create_app()
app.run(debug=True, port=5001)
