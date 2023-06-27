import {FC, useState} from "react"
import styles from "./SwitchRole.module.css"

interface ISwitchRoleProps {
    role: "student" | "teacher"
    setRole: (r: "student" | "teacher") => void
}


const SwitchRole:FC<ISwitchRoleProps> = ({role, setRole}) => {

    return (
        <div>
            <button
                className={role==="student" ? styles.choosen : styles.nonChoosen}
                onClick={() => {setRole("student")}}
            >
                Студент
            </button>
            <button
                className={role==="teacher" ? styles.choosen : styles.nonChoosen}
                onClick={() => {setRole("teacher")}}
            >
                Учитель
            </button>
        </div>
    )
}

export default SwitchRole;
