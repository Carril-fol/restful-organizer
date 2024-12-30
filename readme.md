<p align="center">
  <span style="font-size: 2.5em; font-weight: bold;">Moose Planner API</span>
</p>

**Moose Planner** is an API developed in Flask that provides a platform for organized folder and task management. This API allows users to efficiently structure and manage their tasks, dividing them into folders for better organization and accessibility.

## 📋 Contents

- [✨ Features](#features)
- [🛠️ Tech used](#tech-used)
- [📦 How to get the project:](#how-to-get-the-project)
    - [Using Git (recommended)](#using-git-recommended)
    - [Using manual download ZIP](#using-manual-download-zip)
    - [Using docker](#using-docker)
- [🌐 Deploy in render](#deploy-in-render)
- [API endpoints](#api-endpoints)
    - [*Indication*](#indication)
  - [User related](#user-related)
  - [Folders related](#folders-related)
  - [Tasks related](#tasks-related)

## Features

### 🔒 Authentication 
- Registration of accounts. 
- Login and closing.
- Refreshment of tokens. 

### 📂 Folders Management 
- Create, update and delete folders. 
- See folder details. 

### ✅ Task Management 
- Create tasks associated with folders. 
- View, update and delete tasks.

## Tech used 

**Programming language**
- Python 

**Framework**
- Flask

**Database**
- MongoDB

**Container**
- Docker

## How to get the project
#### Using Git (recommended)
1. Navigate & open CLI into the directory where you want to put this project & Clone this project using this command.
   
```bash
git clone https://github.com/Carril-fol/restful-organizer.git
```
#### Using manual download ZIP
1. Download repository
2. Extract the zip file, navigate into it & copy the folder to your desired directory

#### Using docker
1. Open Docker Desktop
2. Navigate & open CLI of your preference & use this command.
```bash
docker pull carrilfol/restful-organizer
```
3. Now you need to run the image you just downloaded in docker, with the following command
```bash
docker run -p [PORT TO EXPOSE]:5000 carrilfol/restful-organizer
```

## Deploy in render
You can access the live version of the application here (this can be a bit burdensome since the server has to be initialized): 

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://restful-organizer.onrender.com)

## API endpoints

#### *Indication*
- [x] **Authentication required**
- [ ] **Authentication not required**

### User related
- [ ] [Register](docs/auth/UserRegisterResource.md): `POST localhost:[PORT]/users/api/v1/register`
- [ ] [Login](docs/auth/UserLoginResource.md): `POST localhost:[PORT]/users/api/v1/login`
- [x] [Logout](docs/auth/UserLogoutResource.md): `POST localhost:[PORT]/users/api/v1/logout`
- [x] [Get user info](docs/auth/UserDetailsResource.md): `GET localhost:[PORT]/users/api/v1/detail`
- [x] [Refresh token](docs/auth/RefreshTokenResource.md): `POST localhost:[POST]/users/api/v1/refresh`

### Folders related
- [x] [Create a folder](docs/folders/CreateFolderResource.md): `POST localhost:[PORT]/folders/api/v1/create`
- [x] [Get all folder from a user](docs/folders/GetFoldersByUserIdResource.md): `GET localhost:[PORT]/folders/api/v1/user/<user_id>`
- [x] [Detail from a folder](docs/folders/FolderResource.md): `GET localhost:[PORT]/folders/api/v1/<folder_id>`
- [x] [Delete a folder](docs/folders/FolderResource.md): `DELETE localhost:[PORT]/folders/api/v1/<folder_id>`
- [x] [Update a folder](docs/folders/FolderResource.md): `PUT localhost:[PORT]/folders/api/v1/<folder_id>`

### Tasks related
- [x] [Create a task](docs/tasks/CreateTaskResource.md): `POST localhost:[PORT]/tasks/api/v1/<folder_id>`
- [x] [Detail from a tasks](docs/tasks/TaskResource.md): `GET localhost:[PORT]/tasks/api/v1/<task_id>/`
- [x] [Update a task](docs/tasks/TaskResource.md): `PUT localhost:[PORT]/tasks/api/v1/<task_id>`
- [x] [Delete a task](docs/tasks/TaskResource.md): `DELETE localhost:[PORT]/tasks/api/v1/<task_id>`
