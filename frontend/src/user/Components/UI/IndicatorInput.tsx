import {FC, useEffect, useState} from "react";
import styles from "./IndicatorInput.module.css"

interface IInputProps {
    isCorrect: boolean
    type_: "text" | "password"
    value: string
    setValue: (s: string) => void
    placeholder?: string
}


const IndicatorInput:FC<IInputProps> = ({type_, value, setValue, placeholder, isCorrect}) => {

    const [started, setStarted] = useState<boolean>(false);

    return (
        <input
            type={type_}
            value={value}
            onChange={(e) => {setValue(e.target.value)}}
            onFocus={() => {setStarted(true)}}
            placeholder={placeholder}
            className={!started ? styles.input : isCorrect ? styles.inputCorrect : styles.inputIncorrect }
        />
    )
}


export default IndicatorInput;
