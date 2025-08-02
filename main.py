from website import create_app

app = create_app()
# only if we run this file & the web server will this line be executed.
if __name__ == '__main__':
    app.run(debug=True)
    
