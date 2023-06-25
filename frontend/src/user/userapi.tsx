import { IUser } from "./usertypes";

export class UserApi {

    static signIn = async(): Promise<IUser | null> => {
        const response = await fetch(
            "/api/students/me",
            {
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
        )
        if (response.ok) {return await response.json();}
        else {return null;}
    }

}