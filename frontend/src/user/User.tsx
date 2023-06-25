import {FC, PropsWithChildren, ReactElement, ReactNode } from "react"
import { UserProvider } from "./usercontext";



const User:FC = () => {
    return (
        <UserProvider>
            <main>
                User
            </main>
        </UserProvider>
    )
}

export default User;
