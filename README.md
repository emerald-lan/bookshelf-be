# Bookshelf Backend

This is the backend of the bookshelf project, which provides APIs and database management for a web app that allows users to browse and buy books online. We made this project as a way to learn more about e-commerce and to share our love for reading. 📚

🛠 *This repo is still in the development stage. Some features may not work well or may change in the future.*

## Contributors

1. [Bùi Lê Khánh Linh](https://github.com/blkhanhlinh) - Leader / Front-end / Design / Document
2. [Nguyễn Thị Thanh Lan](https://github.com/emerald-lan) - Back-end / Front-end / Document
3. [Nguyễn Duy Ngọc](https://github.com/ngocnd2402) - Document / Back-end

## Installation

1. Create a virtual environment
```sh
py -m venv env
```

2. Activate the virtual env
```sh
.\env\Scripts\activate
```

3. Install dependencies
```sh
pip install -r requirements.txt
cd server
```

4. Run migrations (optional)

If you wish to create a brand new database, feel free to dump the existed sql file and follow the step:

```sh
py manage.py migrate
```

5. Create a superuser account
```sh
py manage.py createsuperuser
```

6. Run the server
```sh
py manage.py runserver
```

Note: You may need to create and provide your infomation in a .env file.

## For contributors

Please create a new branch for your contribution. DO NOT upload code to the `main` branch directly.

📌 Naming branch:

There are 2 types of branches:

-   Feature: This type of branch is for creating a new feature, and the functions should be well described in your Pull Request. Pattern: `feature/name`

-   Fix: Use this type of branch to fix an issue or a set of issues. Pattern: `fix/name`

The branch name will use kebab case: lowercase words and separated by a dash (-). E.g.: feature/example-new-feature

## User interface
- Figma: [Bookshelf UI](https://www.figma.com/file/gNc8HHa4zQJ9MGlXcrPbbY/Bookshelf-%7C-UI%2FUX?type=design&node-id=0%3A1&t=7G7Q4U0cP7a5YQ04-1)