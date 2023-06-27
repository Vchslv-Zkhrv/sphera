
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


export interface StudentShort {
    id: number
    fname: string
    lname: string
}


export interface IGroup {
    id: number
    name: string
    teacher: IUser
    students: StudentShort[]
}
