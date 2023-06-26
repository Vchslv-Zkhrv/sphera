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

    static getNews = 
    async (id: number) => {
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

}