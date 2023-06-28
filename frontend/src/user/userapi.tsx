import { IUser } from "./usertypes";

export class UserApi {

    static signIn = async(): Promise<IUser | null> => {
        const response = await fetch(
            "/api/users/me",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {return await response.json();}
        else {return null;}
    }

    static getFeed = async () => {
        const response = await fetch(
            "/api/feed",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {return await response.json();}
        else {return [];}
    }

    static getNews = async (id: number) => {
        const response = await fetch(
            `/api/feed/${id}`,
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {
            const data = await response.json()
            return data.paragraphs;
        }
        else {return [];}
    }

    static getTags = async () => {
        const response = await fetch(
            "/api/tags/all",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {return await response.json();}
        else {return [];}
    }

    static searchCourses = async (
        tags: number[],
        sort: string,
        desc: boolean
    ) => {
        const response = await fetch(
            `/api/courses/search?desc=${desc}&sort=${sort}`,
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(tags)
            }
        )
        if (response.ok) {return await response.json();}
        else {return [];}
    }

    static getGroups = async () => {
        const response = await fetch(
            "/api/users/me/groups/",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {return await response.json();}
        else {return [];}
    }   

    static createGroup = async (name: string) => {
        const response = await fetch(
            "/api/groups",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name: name})
            }
        )
        return response.status
    }

    static getJoinGropLink = async (id: number) => {
        const response = await fetch(
            `/api/groups/${id}/link`,
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {
            const url = await response.json()
            return url
        }
        else {return null;}
    }

    static banFromGroup = async (gid: number, sid: number) => {
        await fetch(
            `/api/groups/${gid}/students/${sid}`,
            {
                "method": "DELETE",
                "headers": {"Content-Type": "application/json"}
            }
        )
    }

    static logout = async () => {
        await fetch(
            "/api/users/me/cookie",
            { "method": "DELETE", }
        )
    }

    static auth = async (login: string, password: string, role: "student" | "teacher")  => {
        const response = await fetch(
            role==="student" ? "/api/students/me" : "/api/teachers/me",
            {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": JSON.stringify({login, password})
            }
        );
        if (response.ok) {
            return await response.json()
        }
        else {
            return null;
        }
    }

    static signupStudent = async (
        email: string,
        password: string,
        fname: string,
        lname: string,
        sname: string
    ) => {
        const response = await fetch(
            "/api/students",
            {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": JSON.stringify({email, password, fname, lname, sname})
            }
        );
        return response.status
    }

    static getCompanies = async () => {
        const response = await fetch(
            "/api/companies/all/names",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {return await response.json();}
        else {return [];}
    }   

    static getCourse = async (courseId: any) => {
        const response = await fetch(
            `/api/courses/${courseId}`,
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        return response;
    }   

    
    static signupTeacher = async (
        email: string,
        password: string,
        fname: string,
        lname: string,
        sname: string,
        company: number,
        specializations: string[]
    ) => {
        const response = await fetch(
            "/api/students",
            {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": JSON.stringify({email, password, fname, lname, sname, company, specializations, bio:""})
            }
        );
        return response.status
    }

    
    static getGroupSessions = async (groupId: number) =>  {
        const response = await fetch(
            `/api/groups/${groupId}/sessions`,
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) { return await response.json() }
        else {return []}
    }


    static getStudentSessions = async () =>  {
        const response = await fetch(
            "/api/students/me/sessions",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) { return await response.json() }
        else {return []}
    }

    static startGroupSession = async (groupId: any, courseId: any) => {
        const response = await fetch(
            `/api/groups/${groupId}/sessions/?course_id=${courseId}`,
            {
                "method": "POST",
                "headers": {"Content-Type": "application/json"}
            }
        )
        return response.status
    }

}