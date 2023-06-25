
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
