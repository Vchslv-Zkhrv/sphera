import React, {FC, useContext, useEffect, useMemo, useState} from "react";
import styles from './Navbar.module.css';
import { UserContext } from "../../usercontext";
import Logo from "../UI/Logo";
import {Link} from "react-router-dom"
import NavButton from "../UI/NavButton";


interface INavbarProps {
    isShrinked: boolean
    shrink: (b: boolean) => void
}


const Navbar:FC<INavbarProps> = (props) => {

    const {user, setUser} = useContext(UserContext);

    return (
        <nav className={
            user===null ? styles.studentNav:
            user.role == "student" ?
            styles.studentNav: styles.teacherNav
        }>

            <Link to="/" style={{textDecoration: "none"}}>
                <Logo shrink={props.isShrinked} props={{className: props.isShrinked ? styles.logo_shrinked : styles.logo}} />
            </Link>
    
            <ul className={styles.top}>
                <li className={styles.navbutton}>
                    <NavButton
                        text="Поиск материалов"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="telescope"
                        shrink={props.isShrinked}
                        to="/explore"
                    />
                </li>
                <li className={styles.navbutton}>
                    <NavButton
                        text="Мои классы"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="planet-moon"
                        shrink={props.isShrinked}
                        to="/classes"
                    />
                </li>
                <li className={styles.navbutton}>
                    <NavButton
                        text="Мои курсы"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="school"
                        shrink={props.isShrinked}
                        to="/courses"
                    />
                </li>
                <li className={styles.navbutton}>
                    <NavButton
                        text="Мой аккаунт"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="ufo"
                        shrink={props.isShrinked}
                        to="/me"
                    />
                </li>
                <li className={styles.navbutton}>
                    <NavButton
                        text="Чат"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="comment-alt"
                        shrink={props.isShrinked}
                        to="/chat"
                    />
                </li>
            </ul>

            <ul className={styles.bottom}>
                <li className={styles.navbutton}>
                    <NavButton
                        text="О проекте Сфера"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="planet-ringed"
                        shrink={props.isShrinked}
                        to="/about"
                    />
                </li>
                <li className={styles.navbutton}>
                    <NavButton
                        text="Выйти"
                        color={user===null ? "main" : user.role==="student" ? "main" : "alter"}
                        icon="portal-exit"
                        shrink={props.isShrinked}
                        to="/exit"
                    />
                </li>
                
            </ul>

        </nav>
    )
}

export default Navbar;
