import {FC, useEffect } from "react"
import { UserProvider } from "./usercontext";
import { changeFavicon } from "../common/Roles";
import { UserApi } from "./userapi";



const User:FC = () => {

    useEffect(() => {
        changeFavicon("./favicon.ico");
        document.title = "Проект Сфера";
    }, [])

    return (
        <UserProvider>
            <main>
                User
            </main>
        </UserProvider>
    )
}

export default User;
