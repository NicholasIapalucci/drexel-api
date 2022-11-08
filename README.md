# Drexel API

`drexel-api` provides a public API for data related to Drexel University. All data provided by the API is already publicly accessible from Drexel University websites. 

The API provides the following information:

- List of every college in Drexel
    - The name of the major
    - List of every major in the college
        - The name of the major
        - List of every course in the major
            - The code name of the course (such as CS-171)
            - The proper name of the course (such as Computer Programming I)
            - The amount of credits the course is worth
            - The prerequisites for the course
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
    "one of": [
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
    "one of": {
        <prerequisite>, 
        <prerequisite>,
        ...
    }
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
            "one of": [
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

Although the `JSON` files are themselves the API, `drexel-api` also provides a set of JavaScript query methods along with TypeScript declarations. The provided API allows for searching for classes, majors, and colleges by filters:
```ts
let cs171 = courseWith({ properName: "Computer Programming I" });
let arch283 = courseWith({ codeName: "ARCH-283" });

let computerScience = cs171.major;
let CCI = computerScience.college;

let DGA = studentOrganizationWith({ name: "Drexel Gaming Association" });
```
