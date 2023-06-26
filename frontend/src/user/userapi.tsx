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

}