import { FC, useEffect } from "react";
import { changeFavicon } from "../common/Roles";

const Admin:FC = () => {

    useEffect(() => {
        changeFavicon("./favicon_pro.ico");
        document.title = "Администраторы Сфера"
    }, [])

    return (
        <main>
            Admin
        </main>
    )
}

export default Admin;
