import {FC, useEffect, useState} from "react"
import { Link, useLocation } from "react-router-dom"
import styles from "./NavButton.module.css"

interface INavButtonProps {
    to: string
    icon: string
    text: string
    color: "main" | "alter"
    shrink: boolean
}

const NavButton:FC<INavButtonProps> = ({to, text, icon, color, shrink}) => {

    const [isChecked, setChecked] = useState<boolean>(false);
    const location =  useLocation();

    useEffect(() => {
        setChecked(document.location.pathname.startsWith(to))
    }, [location])

    return (
        <Link
            className={
                `${styles.link} ${color==="main" ?
                    isChecked
                        ? styles.main_checked
                        : styles.main_unchecked
                : 
                    isChecked
                        ? styles.alter_checked
                        : styles.alter_unchecked} ${shrink ? styles.shrink : ""}
                `} 
            to={to}
        >
            <img
                src={require(`../../../icons/${color==="main" ? isChecked ? "white" : "black" : isChecked ? "turquoise" : "white"}/${icon}.svg`)}
                style={{maxHeight: 20, maxWidth: 20}}
            />
            {
                !shrink ?
                <p style={{
                    color: color==="main" ? isChecked ? "#FFFFFF" : "#1E1E1E" : isChecked ? "#00929C" : "#FFFFFF",
                    textDecoration: "none",
                    fontWeight: 500
                }}>
                    {text}
                </p>
                :
                <></>
            }
        </Link>
    )
}

export default NavButton;
