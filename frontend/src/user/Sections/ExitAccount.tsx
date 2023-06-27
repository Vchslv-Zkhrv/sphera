import {FC, useEffect} from "react"
import { UserApi } from "../userapi"


const ExitAccount:FC = () => {

    const exit = async () => {
        await UserApi.logout()
        document.location.pathname = "/"
    }

    useEffect(() => {exit()}, [])

    return(
        <></>
    )
}

export default ExitAccount;
