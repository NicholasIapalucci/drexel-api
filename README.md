# drexel-api

`drexel-api` provides a public API for data related to Drexel University. All data provided by the API is already publicly accessible from Drexel University websites. 

The API provides the following information:

- List of every college in Drexel
    - The name of the college
    - List of every major in the college
        - The name of the major
        - List of every course in the major
            - The code name of the course (such as CS-171)
            - The proper name of the course (such as Computer Programming I)
            - The amount of credits the course is worth
            - The prerequisites for the course
    - List of every faculty member in in the college
        - The name of the faculty member
        - The title of the faculty member
        - The email of the faculty member
        - The phone number of the faculty member (if known)
- List of every student organization in Drexel
    - The name of the student organization
    - The description of the student organization

## Prerequisites
The `prerequisites` object provided by each course can come in many forms. That being said, it will always be an array on the outer-most layer. A single prerequisite object has the following form:

```json
{
    "name": "CS-171",
    "minimum grade": "C"
}
```
Some classes allow some choice between prerequisities. In this case, a prerequisite choice object looks like the following: 

```json
{
    "oneOf": [
        <prerequisite>,
        <prerequisite>,
        <prerequisite>,
        ...
    ]
}
```

The prerequisites in `one of` can also contain nested `one ofs`. The top-level prerequisite array then looks something like the following:

```json
[
    <single-prerequisite>,
    <single-prerequisite>,
    "oneOf": [
        <prerequisite>, 
        <prerequisite>,
        ...
    ]
]
```

This can get minorly complicated for certain classes. Here's the format for ARCH-283, for example:

```json
{
    "codeName": "ARCH-283",
    "properName": "Architecture Studio 2C",
    "credits": 4,
    "majorName": "Architecture",
    "prerequisites": [
        {
            "oneOf": [
                [
                    {
                        "codeName": "ARCH-222",
                        "minimum grade": "C-"
                    },
                    {
                        "codeName": "ARCH-252",
                        "minimum grade": "C-"
                    }
                ],
                {
                    "codeName": "ARCH-170",
                    "minimum grade": "C-"
                }
            ]
        },
        {
            "codeName": "ARCH-282",
            "minimum grade": "C-"
        },
        {
            "codeName": "ARCH-225",
            "minimum grade": "C-"
        }
    ]
}
```

## Using the API

The data itself is stored in JSON, which can be accessed in a number of ways. The most simple way to access the API is by using the node module, but other options are available.

### Node.js and TypeScript

Although the `JSON` file contains all of the data for the API, `drexel-api` also provides a set of JavaScript query methods along with TypeScript declarations. Install the API with 

```
npm install drexel-api
```

The provided API allows for searching for classes, majors, and colleges by filters:

```ts
import * as Drexel from "drexel-api";

let cs171 = Drexel.courseWith({ properName: "Computer Programming I" });
let arch283 = Drexel.courseWith({ codeName: "ARCH-283" });

let computerScience = cs171.major;
let CCI = computerScience.college;

let DGA = Drexel.studentOrganizationWith({ name: "Drexel Gaming Association" });
```

This of course only runs on the backend, like any node module. However, `drexel-api` can be run on the front end too. Simply download [the TypeScript file](https://raw.githubusercontent.com/NicholasIapalucci/drexel-api/main/src/index.ts) and [the JSON data](https://raw.githubusercontent.com/NicholasIapalucci/drexel-api/main/src/data/drexel.json) and place them in your project, and you will be able to import them like normal files. If you are not using TypeScript, you can download [the compiled JavaScript file](https://raw.githubusercontent.com/NicholasIapalucci/drexel-api/main/out/index.js) instead.

### Other Uses

The `drexel-api` is written in TypeScript, however the data itself is just a giant JSON file that can be read and parsed by any language. To access the data from another language, simply download [the JSON file](https://raw.githubusercontent.com/NicholasIapalucci/drexel-api/main/src/data/drexel.json) or link to it in your language of choice, and manage the data from there. 
