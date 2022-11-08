// @ts-ignore - if TS tries to typecheck the giant JSON file it dramatically slows down VSCode & intellisense
// Instead manual type checking is set up.
import * as Drexel from "./data/drexel.json" assert { type: "json" };

let colleges = Drexel.colleges as RawCollege[];
let organizations = Drexel.organizations as Organization[];

type OneOrMorePropertiesFrom<T> = Partial<T> & { [K in keyof T]: Pick<T, K> }[keyof { [K in keyof T]: Pick<T, K> }];

type LetterGrade = "A" | "B" | "C" | "D" | "F";
type GradeSign = "-" | "+" | "";
type Grade = `${LetterGrade}${GradeSign}` | "Any";

export interface Organization {
    name: string;
    description: string;
}

export interface Prerequisite {
    codeName: string;
    minimumGrade: Grade;
}

export interface PrerequisiteUnion {
    "one of": (Prerequisite | PrerequisiteUnion)[];
}

interface RawMajor {
    name: string;
    courses: Course[]
}

export interface Major extends RawMajor {
    college: College;
}

export interface RawCollege {
    name: string;
    majors: RawMajor[];
}

export interface College {
    name: string;
    majors: Major[];
}

export class Course {

    /** 
     * The coded name of the course, such as `CS-171` or `ARCH-283`. The code name will always be a nonzero number of
     * capital letters, followed by a hypen and a sequence of digits. In other words, it matches the following regex:
     * ```ts
     * /^[A-Z]+\-\d+$/
     * ```
     */
    public readonly codeName: string;

    /**
     * The proper name of the course, such as "Computer Programming I" or "Architecture Studio 2C".
     */
    public readonly properName: string;

    /**
     * The amount of credits the course is worth. 
     */
    public readonly credits: number;

    /**
     * The direct prerequisites for this course; Those being the prerequisites that do not include prerequisites
     * of prerequisites. 
     */
    public readonly prerequisites: (Prerequisite | PrerequisiteUnion)[]

    /**
     * The major that this course is associated with.
     */
    public readonly major: Major;

    /**
     * The college that this course is from. Equivalent to `course.major.college`. 
     */
    public readonly college: College;

    /**
     * The name of the major this course is associate with. Used to find the `major` object.
     */
    private readonly majorName: string;

    public constructor(properties: {
        codeName: string,
        properName: string,
        credits: number,
        major: Major,
        prerequisites: (Prerequisite | PrerequisiteUnion)[],
    }) {
        Object.keys(properties).forEach(property => this[property] = properties[property]);
        this.college = this.major.college;
    }

    /**
     * Returns whether or not this is a strict prerequisite of the given course. If the prerequisite is this OR
     * another course, this will return false. To check if this can count as a prerequisite towards another course,
     * use `countsTowards()`.
     * 
     * **Parameters**
     * 
     * `course` &mdash; The course to check
     * 
     * **Returns**
     * 
     * Whether or not this course is an absolute requirement to take the given course. 
     */
    public isPrerequisiteOf(course: Course) {
        return course.prerequisites.some(prerequisite => {
            if (prerequisite["codeName"]) return (prerequisite as Prerequisite).codeName === course.codeName;
            return false;
        });
    }

    /**
     * All direct prerequisites of this course; Those being the classes that are absolutely
     * required to be taken by this course. 
     */
    public get allPrerequisites(): Course[] {
        let prerequisites: Course[] = []
        let current: Course[] = [this];
        while (current.length) {
            let next: Course[] = [];
            current.forEach(course => {
                course.prerequisites.filter(prerequisite => {
                    if (prerequisite["codeName"]) {
                        let prerequisiteCourse = courseWith({ codeName: prerequisite["codeName"] })!;
                        prerequisites.push(prerequisiteCourse);
                        next.push(prerequisiteCourse);
                    }
                });
            });
            current = next;
        }
        return prerequisites;
    }

}

/**
 * Returns the first course that matches all of the given filters. This is a particularly slow operation, so
 * use it cautiously. Specifically, for `n` colleges each containing `k` majors each containing `l` courses 
 * tested by `m` filters, in the worst case, this operation will take `n * k * l * m` iterations. 
 * 
 * **Parameters**
 * 
 * `filters` The attributes for the course to have
 * 
 * **Returns**
 * 
 * The first course that matches the given filters.
 * 
 * **Examples**
 * ```ts
 * let cs171 = Course.with({ codeName: "CS-171" });
 * let cs172 = Course.with({ properName: "Computer Programming II" });
 * ```
 */
export function courseWith(filters: OneOrMorePropertiesFrom<Course>): Course | null {
    let correctCourse = null;
    colleges.some(college => {
        return college.majors.some(major => {
            return major.courses.some(course => {
                return Object.keys(filters).filter(filter => filter).every(filter => {
                    if (course[filter] === filters[filter]) {
                        correctCourse = course;
                        return true;
                    }
                    return false;
                });
            });
        });
    });

    return correctCourse;
}

/**
 * Returns all courses that matches all of the given filters. This is a particularly slow operation, so
 * use it cautiously. Specifically, for `n` colleges each containing `k` majors each
 * containing `l` courses tested by `m` filters, this operation will always take `n * k * l * m` iterations. 
 * 
 * **Parameters**
 * 
 * `filters` The attributes for the course to have
 * 
 * **Returns**
 * 
 * All courses that matches the given filters.
 * 
 * **Examples**
 * ```ts
 * 
 * ```
 */
export function coursesWith(filters: OneOrMorePropertiesFrom<Course>): Course[] {
    let correctCourses: Course[] = [];
    colleges.forEach(college => {
        college.majors.forEach(major => {
            major.courses.forEach((course: any) => {
                if (Object.keys(filters).filter(filter => filter).every(filter => filters[filter] === course[filter])) {
                    correctCourses.push(new Course({
                        ...course,
                        major: {...major, college },
                    }));
                }
            });
        });
    });

    return correctCourses;
}

/**
 * Returns the first major that matches the specified filters. 
 * 
 * **Parameters**
 * 
 * `filters` &mdash; The filters that the major must match.
 * 
 * **Returns**
 * 
 * The first major that matches all filters.
 * 
 * **Examples**
 * 
 * ```ts
 * let animation = majorWith({ name: "Animation" });
 * let firstCCImajor = majorWith({ college: "Computing & Informatics" });
 * ```
 */
export function majorWith(filters: OneOrMorePropertiesFrom<Major>): Major | null {
    let correctMajor = null;
    colleges.some(college => {
        return college.majors.some(major => {
            if (Object.keys(filters).every(filter => filters[filter] === major[filter])) {
                correctMajor = major;
                return true;
            }
            return false;
        });
    });

    return correctMajor;
}

/**
 * Returns all majors that matches the specified filters. 
 * 
 * **Parameters**
 * 
 * `filters` &mdash; The filters that the majors must match.
 * 
 * **Returns**
 * 
 * All majors that match the specified filters.
 * 
 * **Examples**
 * 
 * ```ts
 * let CCImajors = majorsWith({ college: "Computing & Informatics" });
 * ```
 */
 export function majorsWith(filters: OneOrMorePropertiesFrom<Major>): Major[] {
    let correctMajors: Major[] = [];
    colleges.forEach(college => {
        return college.majors.forEach(major => {
            if (Object.keys(filters).every(filter => filters[filter] === major[filter])) correctMajors.push({ ...major, college: unrawCollege(college) });
        });
    });

    return correctMajors;
}

function unrawCollege(college: RawCollege): College {
    let unraw: College = { name: college.name, majors: [] };
    college.majors.forEach(major => unraw.majors.push({ ...major, college: unraw }));
    return unraw;
}

/**
 * Returns the first student organization that satisfies all of the following filters. 
 * 
 * ### Parameters
 * 
 * `filters` &mdash; The filters to check each organization with.
 * 
 * ### Returns
 * The first student organization that matches the specified filter. 
 * 
 * ### Time Complexity
 * For `n` organizations in Drexel and `f` filters, the time complexity of this operation is:
 * 
 * Best case: *O(f)*
 * 
 * Worst case: *O(nf)*
 */
export function studentOrganizationWith(filters: OneOrMorePropertiesFrom<Organization>): Organization | null {
    let correctOrganization: Organization | null = null
    organizations.some(organization => {
        if (Object.keys(filters).every(filter => filters[filter] === organization[filter])) {
            correctOrganization = organization;
            return true;
        }
        return false;
    });
    return correctOrganization;
}
