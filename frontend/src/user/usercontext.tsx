import { FC, createContext, PropsWithChildren, useState, ReactNode } from "react";
import { IUser } from "./usertypes";



export const UserContext = createContext<IUser | null>(null);

export const UserProvider: FC<PropsWithChildren> = ({children}) => {

  const [user, setUser] = useState<IUser | null>(null); 

    return (
        <UserContext.Provider value={user}>
            {children}
        </UserContext.Provider>
    )
}
