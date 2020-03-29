import os

from flask import Flask, url_for, render_template
from utils import task_two


def main():
    app = Flask(__name__)

    default_csv = "data.csv"
    abspath = os.path.abspath(os.path.dirname(__file__))
    path_to_csv = os.path.join(abspath, default_csv)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/task2")
    def task_2():
        print(default_csv)
        task2 = task_two(path_to_csv)
        return render_template('task2.html', **task2)

    app.run()


if __name__ == '__main__':
    main()