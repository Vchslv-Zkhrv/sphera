import {FC, useEffect, useState} from "react"
import { Link, useLocation } from "react-router-dom"
import styles from "./NavButton.module.css"

interface IExpandButtonProps {
    color: "main" | "alter"
    shrink: boolean
    setShrink: (b: boolean) => void
}

const ExpandButton:FC<IExpandButtonProps> = ({shrink, color, setShrink}) => {

    const [isChecked, setChecked] = useState<boolean>(false);

    return (
        <button
            onClick={() => {setShrink(!shrink)}}
            className={
                `${
                    styles.link} ${
                    color==="main" ? styles.main_unchecked : styles.alter_unchecked} ${
                    shrink ? styles.shrink : ""}`
                } 
        >
            <img
                src={require(`../../../icons/${color==="main" ? "black" : "white"}/angle-circle-${shrink ? "right" : "left"}.svg`)}
                style={{maxHeight: 20, maxWidth: 20}}
            />
            {
                !shrink
                ?
                <p style={{
                    color: color==="main" ? isChecked ? "#FFFFFF" : "#1E1E1E" : isChecked ? "#00929C" : "#FFFFFF",
                    textDecoration: "none",
                    fontWeight: 500
                }}>
                    Свернуть
                </p>
                :
                <></>
            }
        </button>
    )
}

export default ExpandButton;
