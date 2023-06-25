import { FC, createContext, PropsWithChildren, useState, ReactNode, useEffect } from "react";
import { IUser } from "./usertypes";
import { UserApi } from "./userapi";



export const UserContext = createContext<IUser | null>(null);

export const UserProvider: FC<PropsWithChildren> = ({children}) => {

    const [user, setUser] = useState<IUser | null>(null); 

    const fetchUser = async () => {
        setUser(await UserApi.signIn())
    }

    useEffect(() => {
        fetchUser()
    }, [])

    return (
        <UserContext.Provider value={user}>
            {children}
        </UserContext.Provider>
    )
}
