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

const NavButton:FC<INavButtonProps> = (props) => {

    const [isChecked, setChecked] = useState<boolean>(false);
    const location =  useLocation();

    useEffect(() => {
        setChecked(document.location.pathname.startsWith(props.to))
    }, [location])

    return (
        <Link
            className={
                `${styles.link} ${props.color==="main" ?
                    isChecked
                        ? styles.main_checked
                        : styles.main_unchecked
                : 
                    isChecked
                        ? styles.alter_checked
                        : styles.alter_unchecked} ${props.shrink ? styles.shrink : ""}
                `} 
            to={props.to}
        >
            <img
                src={require(`../../../icons/${props.color==="main" ? isChecked ? "white" : "black" : isChecked ? "turquoise" : "white"}/${props.icon}.svg`)}
                style={{maxHeight: 20, maxWidth: 20}}
            />
            {
                !props.shrink ?
                <p style={{
                    color: props.color==="main" ? isChecked ? "#FFFFFF" : "#1E1E1E" : isChecked ? "#00929C" : "#FFFFFF",
                    textDecoration: "none",
                    fontWeight: 500
                }}>
                    {props.text}
                </p>
                :
                <></>
            }
        </Link>
    )
}

export default NavButton;
