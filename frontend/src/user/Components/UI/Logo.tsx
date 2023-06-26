import {FC, HTMLAttributes, useContext, useEffect, useState} from "react";
import { UserContext } from "../../usercontext";
import { isMobile } from "../../../common/Personalization";

const Logo:FC<{shrink:boolean, props:HTMLAttributes<HTMLImageElement>}> = ({shrink, props}) => {

    const {user, setUser} = useContext(UserContext);
    const [src, setSrc] = useState<any>(null)

    useEffect(() => {
        const size = isMobile() ? "small" : shrink ? "small" : "full"
        const color = user===null ? "main" : user.role==="student" ? "main" : "alter" 
        setSrc(require(`../../../logos/${size}/${color}.png`))
    }, [user, shrink])

    return(
        <img src={src} {...props}/>
    )
}

export default Logo;
