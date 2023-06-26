import { FC, createContext, PropsWithChildren, useState, ReactNode, useEffect } from "react";
import { IUser, IUserContext } from "./usertypes";
import { UserApi } from "./userapi";



export const UserContext = createContext<IUserContext>({user: null, setUser: () => {}});

export const UserProvider: FC<PropsWithChildren> = ({children}) => {

    const [user, setUser] = useState<IUser | null>(null); 

    const fetchUser = async () => {
        setUser(await UserApi.signIn())
        if (user!==null) {
            localStorage.setItem("user", JSON.stringify(user))
        }
    }

    useEffect(() => {
        const localUser = localStorage.getItem("user")
        if (localUser!==null) {
            setUser(JSON.parse(localUser))
        }
        fetchUser()
    }, [])

    return (
        <UserContext.Provider value={{user:user, setUser: (u) => {setUser(u)}}}>
            {children}
        </UserContext.Provider>
    )
}
