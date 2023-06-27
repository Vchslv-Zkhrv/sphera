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

}