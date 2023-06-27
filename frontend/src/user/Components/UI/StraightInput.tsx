import {FC} from "react";
import styles from "./StraightInput.module.css"

interface IInputProps {
    type_: "text" | "password"
    value: string
    setValue: (s: string) => void
    placeholder?: string
}


const StraightInput:FC<IInputProps> = ({type_, value, setValue, placeholder}) => {
    return (
        <input
            type={type_}
            value={value}
            onChange={(e) => {setValue(e.target.value)}}
            placeholder={placeholder}
            className={styles.input}
        />
    )
}


export default StraightInput;
