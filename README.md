# research-paper-graph

# Project Setup
If you are using IntelliJ/PyCharm Professional, you should simply be able to open the project.
You will find some useful run configurations as well.

## Backend
The backend is a Python application with Flask framework.

Some good starting resources are:
 - [The Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
 - [Flask Project Website](https://palletsprojects.com/p/flask/)

If you don't want to use `virtualenv`, you can install the required dependencies with
```
pip install -r requirements.txt
```
Overall, it is advisable to use `virtualenv`.

### Installing new Packages
When installing new packages, make sure that they appear in the `requirements.txt` file

To update the `requirements.txt` file, run
```
pip freeze > requirements.txt
```

### Starting the Backend
To start the backend on a local machine, navigate to the `backend` directory.
Next, activate the `virtualenv` as described before.
Now you can run the backend on [http://localhost:5000](http://localhost:5000) by typing
```
flask run
```

### Linting
This project uses `pylint` as a linter. Simply run
```
pylint app
```
in the `backend` folder.

If you are using IntelliJ , it is recommended to install the [PyLint Plugin](https://plugins.jetbrains.com/plugin/11084-pylint/).


## Frontend
The frontend is located in the `frontend` folder and is written in TypeScript with React.

Some good staring resources are:
 - [The TypeScript Handbook](https://www.typescriptlang.org/)
 - [TypeScript Example on React](https://www.typescriptlang.org/play/index.html?jsx=2&esModuleInterop=true&e=196#example/typescript-with-react)
 - [React + TypeScript Cheatsheets](https://github.com/typescript-cheatsheets/react-typescript-cheatsheet#reacttypescript-cheatsheets)
 - [React: Getting Started](https://reactjs.org/docs/getting-started.html)

### Starting the Frontend
To build the frontend, make sure you have `npm` or `yarn` installed.
Change to the `frontend` directory and run
```
npm install
```
and then
```
npm start
```
Now the frontend should open in your browser.

### Linting
The project uses `tslint`. Run `tslint` with
```
npm run lint
```

If you use `yarn`, issue the same commands but with `yarn` instead of `npm`.

