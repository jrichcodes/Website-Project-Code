from website import create_app, clear_database
import sys

app = create_app()

if (len(sys.argv) > 1) and (sys.argv[1] == "cleardb"):
        clear_database(app);

elif __name__ == '__main__':
    app.run(debug=True)