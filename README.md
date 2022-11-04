# Drexel API

`drexel-api` provides a public API for data related to Drexel University. All data provided by the API is already publicly accessible from Drexel University websites. 

## Colleges & Courses

`drexel-api` provides a `colleges` object that allows enumerating through every college and course provided at drexel. Each `college` object in `colleges` has a number of `course` objects, which each have the code name of the course (such as "CS-171"), the proper name of the course (such as "Computer Programming I"), the number of credits the course is worth, and a list of all prerequisites for the course.

### Prerequisites
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
"ARCH-283": {
    "course name": "Architecture Studio 2C",
    "credits": "4.0",
    "prerequisites": [
        {
            "one of": [
                [
                    {
                        "course name": "ARCH-222",
                        "minimum grade": "C-"
                    },
                    {
                        "course name": "ARCH-252",
                        "minimum grade": "C-"
                    }
                ],
                {
                    "course name": "ARCH-170",
                    "minimum grade": "C-"
                }
            ]
        },
        {
            "course name": "ARCH-282",
            "minimum grade": "C-"
        },
        {
            "course name": "ARCH-225",
            "minimum grade": "C-"
        }
    ]
}
```

## Using the API

Although the `JSON` files are themselves the API, `drexel-api` also provides a set of JavaScript query methods along with TypeScript declarations.

