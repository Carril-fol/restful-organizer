<h1 align="center"> Organizer API REST</h1>

<h4 align="center">A monolithic REST API for managing folders, tasks and events.</h4>

<p align="center">
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="python">
  </a>
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white" alt="mongodb">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify">
    <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white" alt="flask">
  </a>
  <a>
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="docker">
  </a>
  <a>
    <img src="https://img.shields.io/badge/Render-%234f0599.svg?style=for-the-badge&logo=render&logoColor=white" alt="render">
  </a>
</p>

### Contents

- [Features](#features)
- [Tech used](#tech-used)
- [How to get the project:](#how-to-get-the-project)
    - [Using Git (recommended)](#using-git-recommended)
    - [Using manual download ZIP](#using-manual-download-zip)
    - [Using docker](#using-docker)
- [Deploy in render:](#deploy-in-render)
- [API endpoints:](#api-endpoints)
    - [*Indication*](#indication)
  - [User related](#user-related)
  - [Folders related](#folders-related)
  - [Events related](#events-related)
  - [Tasks related](#tasks-related)

## Features

- Register account: Users can register their accounts.
- Login account: Users can log in their accounts.
- Log out account: Users can log out from their accounts.

- Create folders: Users can create folders for they management.
- Update folders: Users can modify they folders.
- Delete folders: Users can delete folders.
- Detail folders: Users can view detailed information about a folder.

- Create tasks: Users can create tasks related to a folder to maintain organization.
- Read tasks: Users can get detail from their tasks.
- Update tasks: Users can modify their task.
- Delete tasks: Users can delete their task.

- Create events: Users can create events related to a folder to maintain organization.
- Read events: Users can get detail from their events.
- Update events: Users can modify their events.
- Delete events: Users can delete their events.

## Tech used 

**Programming language**
- [x] Python 

**Framework**
- [x] Flask

**Database**
- [x] MongoDB

**Container**
- [x] Docker

## How to get the project:
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

## Deploy in render:
You can access the live version of the application here (this can be a bit burdensome since the server has to be initialized): 

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://restful-organizer.onrender.com)

## API endpoints:

#### *Indication*
- [x] **Authentication required**
- [ ] **Authentication not required**

### User related
- [ ] [Register](docs/auth/UserRegisterResource.md): `POST localhost:[PORT]/users/api/v1/register`
- [ ] [Login](docs/auth/UserLoginResource.md): `POST localhost:[PORT]/users/api/v1/login`
- [x] [Logout](docs/auth/UserLogoutResource.md): `POST localhost:[PORT]/users/api/v1/logout`
- [x] [Get user info](docs/auth/UserDetailsResource.md): `GET localhost:[PORT]/users/api/v1/<user_id>`
- [x] [Refresh token](docs/auth/RefreshTokenResource.md): `POST localhost:[POST]/users/api/v1/refresh`

### Folders related
- [x] [Create a folder](docs/folders/CreateFolderResource.md): `POST localhost:[PORT]/folders/api/v1/create`
- [x] [Get all folder from a user](docs/folders/GetFoldersByUserIdResource.md): `GET localhost:[PORT]/folders/api/v1/user/<user_id>`
- [x] [Detail from a folder](docs/folders/FolderResource.md): `GET localhost:[PORT]/folders/api/v1/<folder_id>`
- [x] [Delete a folder](docs/folders/FolderResource.md): `DELETE localhost:[PORT]/folders/api/v1/<folder_id>`
- [x] [Update a folder](docs/folders/FolderResource.md): `PUT localhost:[PORT]/folders/api/v1/<folder_id>`

### Events related
- [x] [Create a event](docs/events/CreateTaskResource.md): `POST localhost:[PORT]/events/api/v1/<folder_id>`
- [x] [Details from a event](docs/events/TaskResource.md): `GET localhost:[PORT]/events/api/v1/<event_id>`
- [x] [Update a event](docs/events/TaskResource.md): `PUT localhost:[PORT]/events/api/v1/<event_id>`
- [x] [Delete a event](docs/events/TaskResource.md): `DELETE localhost:[PORT]/events/api/v1/<event_id>`

### Tasks related
- [x] [Create a task](docs/tasks/CreateTaskResource.md): `POST localhost:[PORT]/tasks/api/v1/<folder_id>`
- [x] [Detail from a tasks](docs/tasks/TaskResource.md): `GET localhost:[PORT]/tasks/api/v1/<task_id>/`
- [x] [Update a task](docs/tasks/TaskResource.md): `PUT localhost:[PORT]/tasks/api/v1/<task_id>`
- [x] [Delete a task](docs/tasks/TaskResource.md): `DELETE localhost:[PORT]/tasks/api/v1/<task_id>`
