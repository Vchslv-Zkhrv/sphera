import {FC} from "react"
import styles from "./Steps.module.css";

interface IStepsProps {
    options: number[]
    current: number
    setCurrent: (n: number) => void
}


const Steps:FC<IStepsProps> = ({options, current, setCurrent}) => {
    return (
        <ul className={styles.steps}>
            {options.map((o) => (
                 <li
                    key={o}
                    className={o==current ? styles.stepCurrent : styles.step}
                    onClick={() => {setCurrent(o)}}
                >
                    {o}
                 </li>
            ))}
        </ul>
    )
}


export default Steps;
