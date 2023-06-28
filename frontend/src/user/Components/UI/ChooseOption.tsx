import {FC} from "react"
import { IOption } from "../../usertypes";
import styles from "./ChooseOption.module.css"


interface IChooseProps {
    options: IOption[]
    current: IOption[]
    setCurrent: (n: IOption[]) => void
    checkboxMode?: boolean
}


const ChooseOption:FC<IChooseProps> = ({options, current, setCurrent, checkboxMode}) => {

    const onSelect = (option: IOption) => {
        if (checkboxMode){

            if (!current.includes(option)) {
                setCurrent([...current, option])
            }
            else {
                let copy = [...current];
                copy.splice(copy.indexOf(option), 1)
                setCurrent([...copy])
            }
        }
        else {
            setCurrent([option, ])
        }
    }


    return (
        <ul className={styles.list}>
            {options.map((o) => (
                <li
                    key={o.id}
                    onClick={() => {onSelect(o)}}
                    className={current.includes(o) ? styles.optionCurrent : styles.option}
                >
                    {o.name}
                </li>
            ))}
        </ul>
    )
}


export default ChooseOption;
