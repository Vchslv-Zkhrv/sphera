import {FC, useEffect, useMemo, useState } from "react"
import { UserProvider } from "./usercontext";
import { changeFavicon } from "../common/Roles";
import Navbar from "./Components/Navbar/Navbar";
import { Route, Routes } from "react-router";
import Home from "./Sections/Home/Home";
import Account from "./Sections/Account/Account";
import Explore from "./Sections/Explore/Explore";
import Chat from "./Sections/Chat/Courses";
import Classes from "./Sections/Classes/Classes";
import Courses from "./Sections/Courses/Courses";
import About from "./Sections/About/About";
import styles from "./User.module.css";


const User:FC = () => {

    const [shrinkNav, setShrinkNav] = useState<boolean>(false);

    useEffect(() => {
        changeFavicon("./favicon.ico");
        document.title = "Проект Сфера";
    }, [])

    return (
        <UserProvider>
            <main className={styles.main}>
                <Navbar isShrinked={shrinkNav} shrink={setShrinkNav}/>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/me" element={<Account/>}/>
                    <Route path="/explore" element={<Explore/>}/>
                    <Route path="/chat" element={<Chat/>}/>
                    <Route path="/classes" element={<Classes/>}/>
                    <Route path="/courses" element={<Courses/>}/>
                    <Route path="/about" element={<About/>}/>
                </Routes>
            </main> 
        </UserProvider>
    )
}

export default User;
