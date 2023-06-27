import { FC, createContext, PropsWithChildren, useState, ReactNode, useEffect } from "react";
import { IUser, IUserContext } from "./usertypes";
import { UserApi } from "./userapi";



export const UserContext = createContext<IUserContext>({user: null, setUser: () => {}});

export const UserProvider: FC<PropsWithChildren> = ({children}) => {

    const [user, setUser] = useState<IUser | null>(null); 

    const fetchUser = async () => {
        setUser(await UserApi.signIn())
    }

    useEffect(() => {
        fetchUser()
    }, [])

    return (
        <UserContext.Provider value={{user:user, setUser: (u) => {setUser(u)}}}>
            {children}
        </UserContext.Provider>
    )
}
