
export interface IUser {
    id: number
    role: "teacher" | "student"
    fname: string
    lname: string
    sname: string
    email: string
    telegram?: number
    company?: string
    specializations?: string[]
    bio?: string
}


export interface IUserContext {
    user: IUser | null
    setUser: (u: IUser | null) => void;
}


export interface INewsParagraph {
    id: number
    kind: "plain text" | "image src"
    content: string
}


export interface INews {
    id: number
    date: Date
    title: string
}


export interface ITag {
    id: number
    name: string
}


export interface ICourseCard {
    id: number
    name: string
    views: number
    tags: ITag[]
}


export interface IUserShort {
    id: number
    fname: string
    lname: string
}


export interface IGroup {
    id: number
    name: string
    teacher: IUser
    students: IUserShort[]
}


export interface IOption {
    id: number
    name: string
}


export interface ILessonShort {
    id: number
    number: number
    name: string
}


export interface ICourse {
    id: number
    name: string
    description: string
    author: IUserShort
    date_created: Date
    date_updated: Date
    views: number
    tags: ITag[]
    lessons: ILessonShort[]
}


export  interface ILesson {
    id: number
    number: number
    name: string
    description: string
    duration: Date
    steps: number[]
}


export interface ICourseShort {
    id: number
    name: string
    views: number
    tags: ITag[]
}


export interface ISession {
    id: number
    date_started: Date
    date_ended: Date
    active: boolean
    course: ICourseShort
}
