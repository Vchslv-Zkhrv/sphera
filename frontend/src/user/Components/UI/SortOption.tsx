import {FC} from "react"
import styles from "./SortOption.module.css"

interface ISortOption {
    active: boolean
    text: string
    value: any
    callback: (a: any) => void
    disabled?: boolean
}


const SortOption:FC<ISortOption> = ({text, value, callback, active, disabled}) => {
    return (
        <button
            onClick={() => {callback(value)}}
            className={active ? styles.optionActive : styles.option}
            disabled={disabled}
        >
            {text}
        </button>
    )
}

export default SortOption;
